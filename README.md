# 🚀 AI Resume Analyser – Powered by Google Gemini LLM

**Smart Resume Analysis & Job Matching Tool**

**Category:** AI/ML Application  
**Created by:** [Ajith Moolya]

---

## 🔍 Problem Statement

Job seekers receive rejections without feedback, making it impossible to know why their resumes don't match job requirements. This creates a frustrating cycle of blind applications without understanding how to improve.

---

## 💡 Solution Overview

**AI Resume Analyser** uses Google Gemini LLM to analyze resumes against job descriptions and provide:
- **ATS match percentage** scoring
- **Missing keywords** identification  
- **Actionable improvement suggestions**
- **Personalized optimization recommendations**

Built with **FastAPI** for robust performance and **Gemini AI** for intelligent analysis.

---

## 🏗️ Architecture

```
Resume + Job Description → FastAPI Backend → Gemini LLM → AI Analysis → Structured Feedback
```

---

## 🛠️ Tools Used

- **FastAPI:** High-performance web framework
- **Google Gemini LLM:** AI analysis engine
- **Python:** Backend development
- **Uvicorn:** ASGI server

---

## 🎯 Core Features

- Upload resume (PDF, DOCX, TXT)
- Paste job description
- Get compatibility score
- Identify missing keywords
- Receive improvement suggestions
- ATS optimization tips

---

## 🔧 Challenges Faced

- Creating effective AI prompts for consistent feedback
- Handling various document formats
- Managing API rate limits
- Ensuring structured response format

---

## 🚀 Future Roadmap

- Multi-language support
- Resume builder integration
- Cover letter analysis
- Mobile app development
- HR dashboard for recruiters

---

## 🔧 Quick Start

```bash
git clone https://github.com/yourusername/ai-resume-analyser.git
cd ai-resume-analyser
pip install -r requirements.txt
# Add Google Gemini API key to .env
uvicorn main:app --reload
```

---

## 🎯 Impact

Transforms resume optimization from guesswork into data-driven improvement, helping job seekers increase interview callbacks and land better opportunities! 🚀

