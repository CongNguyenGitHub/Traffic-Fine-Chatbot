from docx import Document
import json
import re
from sentence_transformers import SentenceTransformer

def extract_text_from_docx(file_path):
    """ Đọc nội dung từ file DOCX và loại bỏ dòng trống """
    doc = Document(file_path)
    return [para.text.strip() for para in doc.paragraphs if para.text.strip()]

def parse_document(text_lines):
    """ Phân tích dữ liệu theo cấu trúc Muc -> Dieu -> Khoan -> NoiDung """
    data = {}
    current_muc, current_dieu, current_khoan = None, None, None

    muc_pattern = re.compile(r'^Mục\s+(\d+)')
    dieu_pattern = re.compile(r'^Điều\s+(\d+)')
    khoan_pattern = re.compile(r'^(\d+)\.\s+(.+)')

    for line in text_lines:
        muc_match = muc_pattern.match(line)
        dieu_match = dieu_pattern.match(line)
        khoan_match = khoan_pattern.match(line)

        if muc_match:
            current_muc = line
            data[current_muc] = {}

        elif dieu_match:
            current_dieu = line
            data[current_muc][current_dieu] = {}

        elif khoan_match:
            current_khoan = f"Khoan_{khoan_match.group(1)}"
            data[current_muc][current_dieu][current_khoan] = {
                "NoiDung": khoan_match.group(2),
                "ChiTiet": []
            }

        elif current_khoan:
            data[current_muc][current_dieu][current_khoan]["ChiTiet"].append(line)

    return data

def process_law_data(data):
    """
    Thêm embedding vào dữ liệu luật dựa trên nội dung và từng chi tiết vi phạm.
    """
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

    count = 0  # Đếm số khoản đã xử lý
    
    for muc, dieu_dict in data.items():
        for dieu, khoan_dict in dieu_dict.items():
            for khoan, details in khoan_dict.items():
                noi_dung = details.get("NoiDung", "")
                
                # Tạo embedding cho từng "ChiTiet" riêng lẻ
                chi_tiet_embeddings = []
                for chi_tiet in details.get("ChiTiet", []):
                    context = f"{muc} {dieu} {khoan} {noi_dung} {chi_tiet}"
                    chi_tiet_embeddings.append(model.encode(context).tolist())
                
                details["Embedding_ChiTiet"] = chi_tiet_embeddings
                count += len(chi_tiet_embeddings)

    print(f"✅ Dữ liệu đã được xử lý ({count} chi tiết).")
    return data

def convert_docx_to_json_with_embeddings(input_docx, output_json):
    """
    Chuyển file DOCX thành JSON, sau đó thêm embeddings và lưu kết quả.
    """
    text_lines = extract_text_from_docx(input_docx)
    structured_data = parse_document(text_lines)
    processed_data = process_law_data(structured_data)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Dữ liệu hoàn chỉnh đã lưu vào {output_json}")

# Chạy chương trình
convert_docx_to_json_with_embeddings("law_data.docx", "law_data_processed.json")
