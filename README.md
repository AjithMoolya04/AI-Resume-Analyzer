# 🚀 AI Resume Analyser – Powered by Google Gemini LLM

**Smart Resume Analysis & Job Matching Tool**

**Category:** AI/ML Application  
**Technology Stack:** FastAPI + Google Gemini LLM  
**Created by:** Ajith Moolya
---

## 🔍 Problem Statement

Job seekers receive rejections without feedback, making it impossible to know why their resumes don't match job requirements. This creates a frustrating cycle of blind applications without understanding how to improve.

---

## 💡 Solution Overview

**AI Resume Analyser** is an intelligent web application that leverages Google's Gemini LLM to provide comprehensive resume analysis and optimization suggestions. The system:

✅ **Analyzes resume-job alignment** with precision scoring  
✅ **Identifies missing keywords** and critical skills gaps  
✅ **Provides actionable improvement suggestions**  
✅ **Offers ATS optimization recommendations**  
✅ **Delivers instant, personalized feedback**

Built with **FastAPI** for robust backend performance and **Google Gemini AI** for advanced natural language understanding, this tool transforms resume optimization from guesswork into a data-driven process.

---

## 🏗️ Architecture/ Data Flow
```mermaid
graph LR
    A["📄 User UploadsResume PDF"] --> B["🔄 PDF Converted toImage/Text"]
    B --> C["🤖 Gemini LLM: Resume + JDAnalysis"]
    C --> D["📊 Match % + Keyword Gaps +Suggestions"]
    D --> E["🌐 FastAPI UI +Results"]
    
    style A fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff
    style B fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff
    style C fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff
    style D fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff
    style E fill:#2d3748,stroke:#4a5568,stroke-width:2px,color:#fff
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

## 🎯 Impact

Transforms resume optimization from guesswork into data-driven improvement, helping job seekers increase interview callbacks and land better opportunities! 🚀

