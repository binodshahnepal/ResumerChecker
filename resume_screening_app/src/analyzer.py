from pathlib import Path
from src.llm_service import get_llm

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "resume_analysis_prompt.txt"


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def analyze_resume(resume_text: str, job_description: str) -> str:
    llm = get_llm()
    template = load_prompt()

    prompt = template.format(
        job_description=job_description,
        resume_text=resume_text
    )

    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)
