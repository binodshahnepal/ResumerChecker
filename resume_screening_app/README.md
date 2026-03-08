# AI Resume Screening App

A Streamlit-based resume screening application that:
- accepts PDF, DOCX, and TXT resumes
- compares a resume against a job description using Gemini
- stores resume chunks in ChromaDB
- supports semantic search over stored resumes

## Features
- Resume upload and text extraction
- Job description based AI analysis
- Chroma vector storage with embeddings
- Semantic recruiter search
- Downloadable AI report

## Project Structure

```text
resume_screening_app/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   ├── uploads/
│   └── reports/
│
├── chroma_store/
├── prompts/
│   └── resume_analysis_prompt.txt
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── resume_loader.py
│   ├── text_processor.py
│   ├── llm_service.py
│   ├── analyzer.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── utils.py
│
└── .streamlit/
    └── config.toml
```

## Setup

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate environment

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Update API key if needed

Edit `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

## Usage
1. Open the app in your browser.
2. Paste a job description.
3. Upload a resume file.
4. Click **Analyze & Store Resume**.
5. Review the AI report.
6. Use the **Search Stored Resumes** tab to semantically search saved resumes.

## Deployment Notes
For Streamlit Community Cloud:
- add your API key in app secrets or environment variables
- persistent local Chroma storage may be limited in hosted environments
- for production, consider external vector DB and cloud storage
