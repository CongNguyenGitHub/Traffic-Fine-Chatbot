from flask import Flask, render_template, request, jsonify
import json
import os
import numpy as np
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load API key từ biến môi trường
load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("API key của Gemini không được tìm thấy trong biến môi trường.")
genai.configure(api_key=GENAI_API_KEY)

# Khởi tạo model Gemini 
gen_model = genai.GenerativeModel('models/gemini-1.5-pro')

# Load model NLP
model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
file_path = "law_data_processed.json"

def load_law_data(file_path):
    """Đọc dữ liệu luật và trích xuất embedding."""
    with open(file_path, "r", encoding="utf-8") as f:
        law_data = json.load(f)

    all_laws, all_embeddings = [], []

    for muc, dieu_data in law_data.items():
        for dieu, khoan_data in dieu_data.items():
            for khoan, details in khoan_data.items():
                noi_dung = details.get("NoiDung", "")
                chi_tiet_list = details.get("ChiTiet", [])
                embeddings_list = details.get("Embedding_ChiTiet", [])
                
                for ct, emb in zip(chi_tiet_list, embeddings_list):
                    all_laws.append({
                        "Muc": muc,
                        "Dieu": dieu,
                        "Khoan": khoan,
                        "NoiDung": noi_dung,
                        "ChiTiet": ct
                    })
                    all_embeddings.append(np.array(emb, dtype=np.float32))

    return all_laws, np.array(all_embeddings, dtype=np.float32)

# Load dữ liệu luật
all_laws, all_embeddings = load_law_data(file_path)

def split_questions_with_gemini(text):
    """Sử dụng Gemini để tách câu hỏi thành các câu nhỏ."""
    prompt = ("Hãy tách đoạn văn bản sau thành các câu hỏi riêng biệt, chỉ trả về danh sách câu hỏi, không thêm giải thích: \n" + text)
    response = gen_model.generate_content(prompt)
    
    if not response.text:
        return [text]  # Trả về câu hỏi gốc nếu Gemini không trả lời
    
    return [q.strip() for q in response.text.split("\n") if q.strip()]

def search_top_k(query, k=5):
    """Tìm kiếm các điều luật liên quan nhất."""
    query_embedding = model.encode(query).reshape(1, -1)
    similarities = cosine_similarity(query_embedding, all_embeddings)[0]
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    
    return [{"similarity": similarities[i], **all_laws[i]} for i in top_k_indices]

def generate_context(query, results):
    """Tạo bối cảnh trả lời dựa trên danh sách điều luật liên quan."""
    context = f"**Câu hỏi:** {query}\n\n **Các điều luật liên quan:**\n"
    for idx, res in enumerate(results, 1):
        context += (f"\n **Luật {idx}:**\n"
                    f" **Mục:** {res['Muc']}\n"
                    f" **Điều:** {res['Dieu']}\n"
                    f" **Khoản:** {res['Khoan']}\n"
                    f" **Nội dung:** {res['NoiDung']}\n")
        if "ChiTiet" in res and res["ChiTiet"]:
            context += f" **Chi tiết:** {res['ChiTiet']}\n"
    return context

def generate_response(context):
    """Sinh phản hồi từ Gemini API."""
    prompt = f"Bạn là chuyên gia luật giao thông, hãy trả lời người dùng dựa trên thông tin sau:\n{context}"
    response = gen_model.generate_content(prompt)
    
    return response.text if response.text else "Xin lỗi, tôi không thể trả lời câu hỏi này."

# Khởi tạo Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Vui lòng nhập câu hỏi hợp lệ."})
    
    # Tách câu hỏi bằng Gemini
    sub_questions = split_questions_with_gemini(user_input)
    all_results = []
    
    for sub_q in sub_questions:
        results = search_top_k(sub_q, k=5)  # Giảm k để tối ưu
        all_results.append(generate_context(sub_q, results))
    
    final_context = "\n\n".join(all_results)
    ai_response = generate_response(final_context)
    
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)