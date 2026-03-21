# 🛡️ AdmitGuard V2

Enterprise Admission Validation Platform — built for IIT cohort Sprint 01

## 🔗 Live Links
- **Frontend:** https://aditi23garg.github.io/admitguard-v2
- **Backend API:** https://admitguard-v2-backend.onrender.com
- **Google Sheet:** https://docs.google.com/spreadsheets/d/1X9aNeRnxxJbb_TAJurWqvf6Frrku4ffU78RrNdt_PN4/edit

## 🏗️ Architecture
Frontend (GitHub Pages) → Backend API (Render/Flask) → Google Sheets

## 🧰 Tech Stack
| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | HTML + CSS + JS | No framework needed, deploys on GitHub Pages |
| Backend | Python Flask | Simple REST API, easy Render deployment |
| Storage | Google Sheets via gspread | Real-time, stakeholder-visible |
| Intelligence | Rule-based scoring | Explainable, no black box |

## ⚙️ Local Setup
1. Clone the repo: `git clone ...`
2. `cd backend && pip install -r requirements.txt`
3. Add `.env` with `SHEET_ID` and `GOOGLE_CREDENTIALS_PATH`
4. Add `credentials.json` from Google Cloud
5. `python app.py`
6. Open `frontend/index.html` in browser

## 🧠 Intelligence Layer
- **Risk Score (0-100):** Computed from education gaps, backlogs, score trends, work experience
- **Category:** Strong Fit / Needs Review / Weak Fit based on score
- **Experience Bucket:** Fresher / Junior / Mid / Senior

