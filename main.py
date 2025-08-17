from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import PyPDF2
import io
import os
from typing import Optional
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Resume Screening Application")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving HTML, CSS, JS
app.mount("/static", StaticFiles(directory="static"), name="static")


load_dotenv()  # make sure this is near the top
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set in the environment!")

genai.configure(api_key=GEMINI_API_KEY)
# # Configure Gemini AI
# GEMINI_API_KEY = "AIzaSyCO4yEBy4p6RAdWDej9QPJIC0sPt6_zVo0"
# genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    resume_text: str

class AnalysisRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = ""

# Global variable to store current resume text
current_resume_text = ""

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def analyze_with_gemini(prompt: str) -> str:
    """Send prompt to Gemini AI and get response"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini AI error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found in static directory</h1>", status_code=404)

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file"""
    global current_resume_text
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    content = await file.read()
    current_resume_text = extract_text_from_pdf(content)
    
    return {"message": "Resume uploaded successfully", "text": current_resume_text}

@app.post("/analyze-resume")
async def analyze_resume(request: dict):
    """Analyze resume based on type"""
    resume_text = request.get("resume_text", "")
    job_description = request.get("job_description", "")
    analysis_type = request.get("analysis_type", "")
    
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is required")
    
    # Check if job description is required for certain analysis types
    if analysis_type in ["keywords", "percentage"] and not job_description.strip():
        raise HTTPException(status_code=400, detail=f"Job description is required for {analysis_type} analysis")
    
    # Focused and concise prompts for each analysis type
    prompts = {
        "about": f"""
        Provide a concise professional summary of this resume in 5-7 bullet points:
        • Current role and experience level
        • Key technical skills
        • Education background
        • Notable achievements (max 2)
        • Overall profile strength
        
        Keep it brief and professional.
        
        Resume: {resume_text}
        """,
        
        "improve": f"""
        Based on this resume, suggest 5-6 specific skill improvements:
        • Technical skills to learn (2-3 specific ones)
        • Certifications to pursue (1-2 relevant ones)
        • Soft skills to develop (1-2 key areas)
        • Industry trends to follow
        
        Be specific and actionable. Focus on current market demands.
        
        Resume: {resume_text}
        {f"Job Context: {job_description}" if job_description.strip() else ""}
        """,
        
        "keywords": f"""
        Compare this resume with the job description and identify:
        • Missing technical keywords (5-6 specific terms)
        • Missing soft skills keywords (2-3 terms)
        • Industry buzzwords to add (3-4 terms)
        • Action verbs to use (3-4 suggestions)
        
        Be specific and list only the most important missing keywords.
        
        Resume: {resume_text}
        Job Description: {job_description}
        """,
        
        "percentage": f"""
        Analyze match percentage between resume and job description. Provide ONLY this format:
        
        MATCH SCORE: X%
        
        BREAKDOWN:
        • Skills Match: X% – Brief explanation in one line
        • Experience Match: X% – Brief explanation in one line  
        • Education Match: X% – Brief explanation in one line
        
        Keep each explanation to maximum 10-12 words. Do not add any other sections.
        
        Resume: {resume_text}
        Job Description: {job_description}
        """
    }
    
    prompt = prompts.get(analysis_type, prompts["about"])
    analysis = analyze_with_gemini(prompt)
    
    return {"analysis": analysis}

@app.post("/custom-query")
async def custom_query(request: QueryRequest):
    """Handle custom queries about the resume"""
    prompt = f"""
    Based on this resume, answer the following question concisely and helpfully:
    
    Question: {request.query}
    
    Resume: {request.resume_text}
    
    Provide a focused, practical response in 3-5 sentences.
    """
    
    response = analyze_with_gemini(prompt)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)