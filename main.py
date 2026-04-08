from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import fitz  # PyMuPDF
from docx import Document
from typing import Dict, List, Tuple

app = FastAPI(title="AI Resume Analyzer (Nepal Students)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Nepal student friendly job role skill maps ---
ROLE_SKILLS: Dict[str, List[str]] = {
    "data_analyst": [
        "excel", "sql", "python", "power bi", "tableau", "statistics", "data cleaning",
        "pandas", "numpy", "dashboard", "visualization"
    ],
    "backend_developer": [
        "python", "django", "fastapi", "rest", "api", "postgresql", "mysql",
        "docker", "git", "authentication", "jwt"
    ],
    "frontend_developer": [
        "javascript", "react", "html", "css", "tailwind", "typescript", "redux",
        "responsive", "api", "ui"
    ],
    "devops": [
        "linux", "docker", "kubernetes", "ci/cd", "github actions", "aws", "nginx",
        "monitoring", "terraform"
    ],
    "ui_ux": [
        "figma", "wireframe", "prototype", "user research", "ux", "ui", "design system",
        "usability", "typography"
    ],
}

# ATS sections usually expected
REQUIRED_SECTIONS = {
    "contact": [r"email", r"phone", r"linkedin|github|portfolio"],
    "summary": [r"summary|objective|profile"],
    "education": [r"education|academic"],
    "skills": [r"skills|technical skills|tools"],
    "experience": [r"experience|work experience|internship"],
    "projects": [r"projects|project"],
}

ACTION_VERBS = [
    "built", "developed", "designed", "created", "implemented", "improved", "optimized",
    "analyzed", "led", "managed", "deployed", "tested", "automated", "collaborated"
]

BAD_SIGNS = [
    ("too_many_images", "If your resume is mostly images, ATS may fail to read it. Use text-based resume."),
    ("no_metrics", "Add numbers like 'improved by 20%', 'handled 50+ records', etc. It increases impact."),
    ("missing_links", "Add GitHub/LinkedIn/Portfolio links if you have them."),
]

# ---------- File text extraction ----------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts).strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    # python-docx needs a file-like object; simplest is to save temp in memory using bytes -> Document via stream
    import io
    f = io.BytesIO(file_bytes)
    doc = Document(f)
    parts = []
    for p in doc.paragraphs:
        if p.text:
            parts.append(p.text)
    return "\n".join(parts).strip()

def normalize(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

# ---------- Simple NLP helpers ----------
def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))

def find_emails(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

def find_phone_numbers(text: str) -> List[str]:
    # Nepal-friendly loose match: 98xxxxxxxx, 97xxxxxxxx, etc. or +977...
    phones = re.findall(r"(?:\+977[- ]?)?\b9[678]\d{8}\b", text)
    return list(set(phones))

def contains_any(patterns: List[str], text: str) -> bool:
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False

def skill_match(text: str, role: str) -> Tuple[int, List[str], List[str]]:
    role = role.lower().strip()
    skills = ROLE_SKILLS.get(role, [])
    if not skills:
        return 0, [], []

    found = []
    missing = []
    low = text.lower()
    for s in skills:
        # simple contains check; good enough for MVP
        if s.lower() in low:
            found.append(s)
        else:
            missing.append(s)

    score = round((len(found) / max(len(skills), 1)) * 100)
    return score, found, missing

def ats_score(text: str, role: str) -> Dict:
    low = text.lower()

    # 1) Sections score
    sections_found = {}
    missing_sections = []
    for section, patterns in REQUIRED_SECTIONS.items():
        ok = contains_any(patterns, low)
        sections_found[section] = ok
        if not ok:
            missing_sections.append(section)

    section_score = round((sum(1 for v in sections_found.values() if v) / len(REQUIRED_SECTIONS)) * 40)

    # 2) Contact score (email + phone + link)
    email_ok = len(find_emails(text)) > 0
    phone_ok = len(find_phone_numbers(text)) > 0
    link_ok = bool(re.search(r"(linkedin\.com|github\.com|portfolio|behance\.net|dribbble\.com)", low))
    contact_score = (10 if email_ok else 0) + (7 if phone_ok else 0) + (8 if link_ok else 0)  # max 25

    # 3) Keyword match score (role)
    role_score, found_skills, missing_skills = skill_match(text, role)
    keyword_score = round((role_score / 100) * 25)  # max 25

    # 4) Quality signals (verbs + metrics)
    verbs_found = sum(1 for v in ACTION_VERBS if re.search(rf"\b{re.escape(v)}\b", low))
    verb_score = min(10, verbs_found)  # cap 10

    metrics_ok = bool(re.search(r"\b(\d+%|\d+\+|\d{2,})\b", text))  # 20%, 50+, 100 etc.
    metrics_score = 10 if metrics_ok else 0

    quality_score = verb_score + metrics_score  # max 20

    total = section_score + contact_score + keyword_score + quality_score
    total = min(100, total)

    # feedback bullets
    feedback = []

    # Missing sections feedback (Nepal student friendly)
    section_names = {
        "contact": "Contact (email/phone/links)",
        "summary": "Summary / Objective",
        "education": "Education",
        "skills": "Skills",
        "experience": "Experience / Internship",
        "projects": "Projects"
    }
    for ms in missing_sections:
        feedback.append(f"Add a clear **{section_names.get(ms, ms)}** section. ATS systems look for these headings.")

    if not email_ok:
        feedback.append("Add a professional email (example: firstname.lastname@gmail.com).")
    if not phone_ok:
        feedback.append("Add your phone number (Nepal format like 98XXXXXXXX).")
    if not link_ok:
        feedback.append("Add LinkedIn/GitHub/Portfolio link if you have one.")

    if role and role in ROLE_SKILLS and len(found_skills) < max(3, len(ROLE_SKILLS[role]) // 3):
        feedback.append(f"For the role **{role.replace('_',' ')}**, include more relevant skills/keywords (but only if you actually know them).")

    if not metrics_ok:
        feedback.append("Add measurable impact: numbers like users, time saved, accuracy, % improvement, etc.")

    # Keep resume length guidance
    words = count_words(text)
    if words < 180:
        feedback.append("Your resume looks too short. Add more detail about projects, tech stack, and what you achieved.")
    elif words > 900:
        feedback.append("Your resume looks too long. Keep it 1 page if you are a student or fresher (unless you have strong experience).")

    # Suggested keywords: choose top missing role skills
    suggested_keywords = missing_skills[:10] if missing_skills else []

    return {
        "ats_score": total,
        "breakdown": {
            "sections_score_out_of_40": section_score,
            "contact_score_out_of_25": contact_score,
            "keyword_score_out_of_25": keyword_score,
            "quality_score_out_of_20": quality_score,
        },
        "sections_found": sections_found,
        "missing_sections": missing_sections,
        "role": role,
        "role_skill_match_percent": role_score,
        "skills_found": found_skills,
        "skills_missing": missing_skills,
        "suggested_keywords": suggested_keywords,
        "feedback": feedback[:12],  # keep it clean
        "stats": {
            "word_count": words,
            "emails_found": find_emails(text),
            "phones_found": find_phone_numbers(text),
        }
    }

# ---------- API ----------
class AnalyzeResponse(BaseModel):
    ats_score: int
    breakdown: Dict
    sections_found: Dict[str, bool]
    missing_sections: List[str]
    role: str
    role_skill_match_percent: int
    skills_found: List[str]
    skills_missing: List[str]
    suggested_keywords: List[str]
    feedback: List[str]
    stats: Dict

@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer (Nepal Students) is running ✅",
        "endpoints": {
            "POST /analyze": "Upload resume (pdf/docx) + role to get score + feedback"
        },
        "roles_supported": list(ROLE_SKILLS.keys())
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    role: str = Form("data_analyst"),
    file: UploadFile = File(...)
):
    file_bytes = await file.read()
    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    else:
        # try to handle as plain text
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    text = normalize(text)

    if not text or count_words(text) < 30:
        return AnalyzeResponse(
            ats_score=0,
            breakdown={},
            sections_found={},
            missing_sections=[],
            role=role,
            role_skill_match_percent=0,
            skills_found=[],
            skills_missing=[],
            suggested_keywords=[],
            feedback=["Could not read enough text from this resume. If it's scanned image, convert to text-based PDF or use DOCX."],
            stats={"word_count": count_words(text)}
        )

    result = ats_score(text, role)
    return AnalyzeResponse(**result)
    