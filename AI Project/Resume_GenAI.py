import google.generativeai as genai
import pdfplumber
from docx import Document

# 🔹 Configure Google Gemini API Key
genai.configure(api_key="API_KEY")

# 🔹 Use the correct model
model = genai.GenerativeModel("gemini-1.5-pro-latest")


# 🔹 Function to extract text from a PDF resume
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return '\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])


# 🔹 Function to extract text from a DOCX resume
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return '\n'.join([para.text for para in doc.paragraphs])


# 🔹 Function to analyze resume details using Gemini
def analyze_resume(text):
    prompt = f"""
    Extract the following details from the resume text:
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


# 🔹 Function to match candidate with job description
def match_candidate_to_job(resume_text, job_description):
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


# 🔹 Main Execution Flow
if __name__ == "__main__":
    # Set the resume file path (Change to DOCX if needed)
    resume_path = r"C:\Users\Meghananda\Downloads\project_manager_resume.pdf"

    # Extract resume text
    resume_text = extract_text_from_pdf(resume_path)  # Use extract_text_from_docx() if DOCX

    # Define job description
    job_description = "Looking for a Project manager with 6+ years of experience in Software development."

    # Analyze Resume
    analysis = analyze_resume(resume_text)
    match_score = match_candidate_to_job(resume_text, job_description)

    # Display Results
    print("\n🔹 Resume Analysis:\n", analysis)
    print("\n🔹 Match Score:\n", match_score)
