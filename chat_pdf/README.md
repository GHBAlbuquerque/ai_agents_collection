# 📄 Chat PDF

An intelligent PDF document analyzer with an interactive web interface. Chat PDF allows users to upload PDF files and ask questions about their content, powered by AI agents and LangChain.

## 🎯 Features

- **PDF Upload & Analysis:** Upload and process PDF documents
- **Conversational Interface:** Ask questions about your PDF content in natural language
- **AI-Powered Responses:** Leverages LangChain for intelligent document understanding
- **User-Friendly UI:** Streamlit-based interface for seamless interaction

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Web UI)
* **Backend:** Python
* **AI Framework:** LangChain
* **LLM Integration:** OpenAI API (or compatible LLM provider)

## ⚙️ How to Run

1. **Environment Setup:** Ensure you have a `.env` file with your API keys configured (e.g., `OPENAI_API_KEY`)

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```
3. Start the Application:
```bash
python -m streamlit run Home.py
```
4. Access the Interface: Open your browser and navigate to the displayed Streamlit URL (typically http://localhost:8501)

## 💡 How to Use
1. Launch the application using the command above
2. Upload a PDF file using the file uploader in the sidebar
3. Ask questions about the PDF content in the chat interface
4. Receive AI-generated answers based on the document analysis
5. Prompt and Message History can be debugged on `Debug` page
6. Change settings like model, search type and search args on the `Settings` page

-----------------------------------
Developed with ❤️ by [@GHBAlbuquerque](https://github.com/GHBAlbuquerque)