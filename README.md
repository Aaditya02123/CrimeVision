# CrimeVision AI – Intelligent Multimodal Forensic Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF.svg)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google_Gemini-1.5_Pro_%2F_Flash-8E75C2.svg)](https://ai.google.dev)
[![ReportLab](https://img.shields.io/badge/PDF_Engine-ReportLab-0284c7.svg)](https://www.reportlab.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**CrimeVision AI** is an enterprise-grade multimodal criminalistics and forensic intelligence platform. It bridges high-resolution crime scene vision analysis, acoustic telemetry & speaker transcription, surveillance video action detection, automated timeline fusion, legal crime classification, and an interactive investigative AI copilot into a unified tactical workstation.

---

## 🌟 Production Deployment Architecture

This repository is built for **1-Click Full-Stack Vercel Deployment**:
- **Modern React 19 + Vite + Tailwind CSS** frontend communicating with a high-performance **FastAPI (Python)** backend via strict JSON contracts (`vercel.json`).
- Legacy/local Streamlit files (`streamlit_app.py`, `styles.css`, `.streamlit/`) are excluded via `.gitignore` to keep deployments lightweight and prevent serverless bundle size limits.

---

## 📂 Project Directory Layout

```
CrimeVision/
├── api/
│   └── index.py                     # Vercel serverless function entrypoint
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── audio.py             # /api/v1/analyze/audio (Gemini Audio)
│   │   │   ├── cases.py             # /api/v1/cases (CRUD & case statistics)
│   │   │   ├── chat.py              # /api/v1/chat (Investigator AI Copilot)
│   │   │   ├── fusion.py            # /api/v1/fusion/timeline & /classify
│   │   │   ├── image.py             # /api/v1/analyze/image (Gemini Vision)
│   │   │   ├── report.py            # /api/v1/report/generate & /download
│   │   │   └── video.py             # /api/v1/analyze/video (Surveillance telemetry)
│   │   ├── services/
│   │   │   ├── fusion_engine.py     # Chronological fusion & incident classifier
│   │   │   ├── gemini_service.py    # Google GenAI SDK integration
│   │   │   ├── mock_service.py      # High-fidelity forensic fallback generator
│   │   │   └── pdf_generator.py     # ReportLab multi-page PDF generator
│   │   ├── config.py                # Database paths, uploads dir, Gemini settings
│   │   ├── database.py              # SQLite schema & query managers
│   │   ├── models.py                # Pydantic validation request/response schemas
│   │   └── main.py                  # Core FastAPI application instance
│   ├── reports/                     # Generated PDF dossiers
│   ├── uploads/                     # Ingested forensic media files
│   ├── forensic_data.db             # Pre-seeded SQLite database
│   ├── main.py                      # FastAPI entrypoint exporting app
│   ├── app.py                       # Vercel ASGI export
│   ├── index.py                     # Vercel ASGI export
│   ├── requirements.txt             # Backend dependencies
│   └── .env.example                 # Environment configuration template
├── frontend/                        # Decoupled React 19 + Vite + Tailwind CSS UI
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── DashboardOverview.jsx
│   │   │   ├── EvidenceVision.jsx
│   │   │   ├── AudioForensics.jsx
│   │   │   ├── VideoSurveillance.jsx
│   │   │   ├── TimelineFusion.jsx
│   │   │   ├── CopilotChat.jsx
│   │   │   ├── ReportGenerator.jsx
│   │   │   └── DisclaimerBanner.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── sample_data/                     # Pre-packaged sample forensic assets
├── app.py                           # Top-level Vercel gateway proxy
├── requirements.txt                 # Top-level deployment dependencies
├── vercel.json                      # Vercel deployment configuration
├── run_backend.bat                  # Launcher for FastAPI backend
├── run_frontend.bat                 # Launcher for React + Vite frontend
├── start_platform.bat               # 1-Click launcher for both backend & frontend
└── README.md
```

---

## 💻 Running the Application Locally

### 1. Run Both Servers with One Click
```bash
.\start_platform.bat
```
*Launches both the FastAPI backend (port 8000) and the React + Vite frontend (port 5173).*

### 2. Or Run Individual Components

#### FastAPI Backend:
```bash
# Using batch launcher:
.\run_backend.bat

# Or manual command:
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
- API Server: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`

#### React + Vite Frontend:
```bash
# Using batch launcher:
.\run_frontend.bat

# Or manual command:
cd frontend
npm install
npm run dev
```
- Access at: `http://localhost:5173`

---

## 🚀 Deploying to Vercel

This repository is pre-configured with `vercel.json` for multi-service deployment:

1. Push your repository to GitHub.
2. Import the project into **[Vercel](https://vercel.com/)**.
3. In Project Settings, set environment variables:
   - `GEMINI_API_KEY`: *(Optional, will fall back to high-fidelity Sandbox mode if not provided)*
   - `GEMINI_MODEL`: `gemini-1.5-flash`
4. Deploy! Vercel automatically deploys the React Vite frontend and the Python FastAPI backend.
