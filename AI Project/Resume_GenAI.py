import google.generativeai as genai
import pdfplumber
from docx import Document
import os

# Configure Google Gemini API
API_KEY = "API_KEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    with pdfplumber.open(pdf_path) as pdf:
        return '\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])


def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file"""
    doc = Document(docx_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def extract_resume_text(file_path):
    """Automatically extract text based on file type (PDF or DOCX)"""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")


def analyze_resume(text):
    """Analyze resume content using Google Gemini AI"""
    prompt = f"""
    Extract the following details from the resume:
    - Name
    - Email
    - Phone Number
    - Skills
    - Experience (years)
    - Education

    Resume Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text


def match_candidate_to_job(resume_text, job_description):
    """Compare resume with job description and score the match."""
    prompt = f"""
    Compare the following resume with the job description.
    Score the candidate out of 100 based on skill and experience match.

    Resume Text:
    {resume_text}

    Job Description:
    {job_description}
    """
    response = model.generate_content(prompt)
    return response.text


# Example Usage
resume_path = "C:/Users/Meghananda/Downloads/sample_resume.pdf"  # Change file path
resume_text = extract_resume_text(resume_path)
job_description = "Looking for a Python Developer with 3+ years of experience in AI/ML."

analysis = analyze_resume(resume_text)
match_score = match_candidate_to_job(resume_text, job_description)

print("Resume Analysis:\n", analysis)
print("Match Score:\n", match_score)
