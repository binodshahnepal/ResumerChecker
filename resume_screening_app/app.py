import os
import streamlit as st

from src.config import UPLOAD_DIR, REPORT_DIR
from src.utils import ensure_directories
from src.resume_loader import load_resume
from src.text_processor import clean_text, split_text
from src.analyzer import analyze_resume
from src.vector_store import store_resume_chunks
from src.retriever import search_resumes

ensure_directories([UPLOAD_DIR, REPORT_DIR])

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #081120 0%, #0b1324 45%, #0f172a 100%);
        color: #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .topbar {
        background: linear-gradient(135deg, rgba(37,99,235,0.18), rgba(124,58,237,0.14));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.20);
        margin-bottom: 1rem;
    }

    .topbar-title {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.35rem;
        line-height: 1.1;
    }

    .topbar-subtitle {
        font-size: 1rem;
        color: #cbd5e1;
        line-height: 1.6;
    }

    .pill-row {
        margin-top: 0.9rem;
    }

    .pill {
        display: inline-block;
        padding: 0.38rem 0.82rem;
        margin-right: 0.45rem;
        margin-bottom: 0.45rem;
        border-radius: 999px;
        font-size: 0.82rem;
        color: #dbeafe;
        background: rgba(59,130,246,0.14);
        border: 1px solid rgba(96,165,250,0.18);
    }

    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1rem 1rem 0.9rem 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.16);
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: white;
        font-size: 1.55rem;
        font-weight: 800;
    }

    .main-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 1.2rem;
        box-shadow: 0 10px 26px rgba(0,0,0,0.18);
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }

    .side-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1rem;
        box-shadow: 0 8px 22px rgba(0,0,0,0.16);
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.25rem;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 0.96rem;
        margin-bottom: 1rem;
    }

    .helper-title {
        color: white;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .helper-box {
        background: rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 0.9rem;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.8rem;
    }

    .helper-text {
        color: #cbd5e1;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .stTextArea label, .stFileUploader label, .stTextInput label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 18px !important;
        background: rgba(255,255,255,0.96) !important;
        color: #111827 !important;
        padding: 1rem !important;
        font-size: 0.98rem !important;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 14px !important;
        background: rgba(255,255,255,0.96) !important;
        color: #111827 !important;
        padding: 0.8rem !important;
    }

    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.04);
        border: 1px dashed rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 0.45rem;
    }

    div.stButton > button {
        width: 100%;
        height: 3rem;
        border-radius: 14px;
        border: none;
        font-weight: 700;
        color: white;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        box-shadow: 0 8px 20px rgba(37,99,235,0.25);
    }

    div.stDownloadButton > button {
        width: 100%;
        height: 3rem;
        border-radius: 14px;
        border: none;
        font-weight: 700;
        color: white;
        background: linear-gradient(90deg, #0891b2, #06b6d4);
        box-shadow: 0 8px 20px rgba(8,145,178,0.25);
    }

    .report-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1rem;
        color: #f8fafc;
        line-height: 1.75;
        white-space: pre-wrap;
    }

    .search-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    .search-title {
        font-size: 1rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.55rem;
    }

    .search-meta {
        color: #93c5fd;
        font-size: 0.87rem;
        margin-bottom: 0.65rem;
    }

    .search-text {
        color: #dbe4ee;
        font-size: 0.93rem;
        line-height: 1.65;
    }

    .footer-note {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 1.2rem;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.7rem;
            padding-right: 0.7rem;
            padding-top: 0.7rem;
        }

        .topbar {
            padding: 1rem;
            border-radius: 20px;
        }

        .topbar-title {
            font-size: 1.55rem;
        }

        .topbar-subtitle {
            font-size: 0.92rem;
        }

        .main-card, .side-card, .metric-card {
            border-radius: 18px;
            padding: 0.95rem;
        }

        .section-title {
            font-size: 1.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="topbar">
    <div class="topbar-title">AI Resume Screening Platform</div>
    <div class="topbar-subtitle">
        Screen resumes, compare them against job descriptions, store embeddings in a vector database,
        and search candidates semantically with a recruiter-friendly workflow.
    </div>
    <div class="pill-row">
        <span class="pill">Gemini AI</span>
        <span class="pill">LangChain</span>
        <span class="pill">ChromaDB</span>
        <span class="pill">Semantic Search</span>
        <span class="pill">Mobile Ready</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- METRICS --------------------
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Workflow</div>
        <div class="metric-value">Analyze</div>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Storage</div>
        <div class="metric-value">ChromaDB</div>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Search Mode</div>
        <div class="metric-value">Semantic</div>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Resume Analysis", "Search Candidates"])

# -------------------- TAB 1 --------------------
with tab1:
    left, right = st.columns([1.65, 0.95], gap="large")

    with left:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Analyze Resume Against Job Description</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Paste the job description, upload a resume, and generate an AI screening report.</div>', unsafe_allow_html=True)

        job_description = st.text_area(
            "Job Description",
            height=260,
            placeholder="Paste the full job description here..."
        )

        uploaded_file = st.file_uploader(
            "Upload Resume (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"]
        )

        analyze_clicked = st.button("Analyze & Store Resume")

        if analyze_clicked:
            if not uploaded_file:
                st.error("Please upload a resume.")
            elif not job_description.strip():
                st.error("Please paste a job description.")
            else:
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                try:
                    with st.spinner("Reading resume..."):
                        raw_text = load_resume(file_path)

                    if not raw_text.strip():
                        st.error("Resume text could not be extracted.")
                    else:
                        cleaned_text = clean_text(raw_text)
                        chunks = split_text(cleaned_text)

                        with st.spinner("Analyzing with Gemini..."):
                            report = analyze_resume(cleaned_text, job_description)

                        metadata = {"file_name": uploaded_file.name}

                        with st.spinner("Storing embeddings in Chroma..."):
                            store_resume_chunks(chunks, metadata)

                        st.success("Resume analyzed and stored successfully.")
                        st.markdown("### Screening Report")
                        st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.download_button(
                            label="Download Report",
                            data=report,
                            file_name=f"{uploaded_file.name}_analysis.txt",
                            mime="text/plain"
                        )

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="side-card">', unsafe_allow_html=True)
        st.markdown('<div class="helper-title">How it works</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="helper-box">
            <div class="helper-text">
                1. Paste the job description<br>
                2. Upload the candidate resume<br>
                3. Generate an AI screening report<br>
                4. Store resume embeddings for later search
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="helper-title">Best results</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="helper-box">
            <div class="helper-text">
                Use complete job descriptions with role, skills, qualifications,
                experience requirements, and preferred technologies.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="helper-title">Supported files</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="helper-box">
            <div class="helper-text">
                PDF, DOCX, and TXT resumes are supported. Cleanly formatted resumes
                usually produce better extraction and more reliable screening reports.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------- TAB 2 --------------------
with tab2:
    top_left, top_right = st.columns([1.5, 0.8], gap="large")

    with top_left:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Search Stored Candidates</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Use natural language to find matching candidates from stored resumes.</div>', unsafe_allow_html=True)

        query = st.text_input(
            "Search Query",
            placeholder="Example: Python developer with Docker and AWS"
        )

        search_clicked = st.button("Search Candidates")

        if search_clicked:
            if not query.strip():
                st.error("Please enter a search query.")
            else:
                try:
                    results = search_resumes(query, k=5)

                    if not results:
                        st.warning("No matching resumes found.")
                    else:
                        st.success(f"Found {len(results)} result(s).")

                        for i, doc in enumerate(results, start=1):
                            file_name = doc.metadata.get("file_name", "Unknown")
                            snippet = doc.page_content[:700] + ("..." if len(doc.page_content) > 700 else "")

                            st.markdown(f"""
                            <div class="search-card">
                                <div class="search-title">Candidate Match {i}</div>
                                <div class="search-meta">File: {file_name}</div>
                                <div class="search-text">{snippet}</div>
                            </div>
                            """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Search failed: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    with top_right:
        st.markdown('<div class="side-card">', unsafe_allow_html=True)
        st.markdown('<div class="helper-title">Search ideas</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="helper-box">
            <div class="helper-text">
                • Python developer with AWS<br>
                • Data scientist with NLP experience<br>
                • Backend engineer with microservices<br>
                • Candidate with Docker and Kubernetes
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="helper-title">Why semantic search?</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="helper-box">
            <div class="helper-text">
                The search is embedding-based, so it can retrieve relevant candidates
                even when the wording in the resume is slightly different from the query.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="footer-note">Built with Streamlit, Gemini, LangChain and ChromaDB</div>', unsafe_allow_html=True)