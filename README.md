# AI-Powered Legal Chatbot

## Overview
This project is an AI-powered chatbot designed to answer questions related to administrative penalties for traffic violations. It leverages NLP and AI models to provide accurate and context-aware responses based on legal documents.

## Features
- **Web-based AI Chatbot**: Developed using **Flask** for the backend and **HTML/CSS/JavaScript** for the frontend.
- **AI/ML Integration**: Utilizes **Google Gemini API** for natural language processing and **Sentence-BERT** for question similarity detection.
- **Database Management**: Stores legal data in a structured JSON format.
- **Full Stack Development**: Implemented with Python (Flask), JavaScript (React/Node.js in future updates), and SQL for data management.


## Technologies Used
- **Frontend**: HTML, CSS, JavaScript (React in future updates)
- **Backend**: Flask (Python), Node.js (for API handling)
- **Database**: JSON-based structured storage (with future support for SQL/NoSQL databases)
- **AI/ML**:
  - **Sentence-BERT** for question encoding
  - **Google Gemini API** for intelligent responses
  - **Scikit-learn** for similarity computations

## Demo Web Application
**Here’s a screenshot of the web application interface:**


## Installation
### Prerequisites
- Python 3.8+
- Node.js & npm (for frontend development)
- Virtual Environment (Recommended)
- API Key for Google Gemini API

### Steps to Run the Project
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/ai-legal-chatbot.git
   cd ai-legal-chatbot
   ```
2. **Set Up the Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables**
   Create a `.env` file and add your Google API key:
   ```
   GENAI_API_KEY=your_api_key_here
   ```
5. **Run the Application**
   ```bash
   flask run
   ```
6. **Access the Web App**
   Open `http://127.0.0.1:5000/` in your browser.


## Future Improvements
- **Expand AI Capabilities**: Improve chatbot reasoning using fine-tuned LLM models.
- **Enhance UI/UX**: Integrate with React.js.
- **Cloud Hosting**: Deploy on **Azure** with Databricks support.

## Contributors
- **Nguyen Cong Nguyen**

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

