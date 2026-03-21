# 🛡️ AdmitGuard V2
### Enterprise Admission Validation Platform

> Solving unreliable and unstructured admission data collection in Indian higher education — by automating validation, flagging risky applications, and consolidating data in real time.

---

## 🔗 Live Links
| Resource | URL |
|----------|-----|
| 🌐 Frontend | https://aditi23garg.github.io/admitguard-v2/ |
| ⚙️ Backend API | https://admitguard-v2-backend.onrender.com |
| 📊 Google Sheet | https://docs.google.com/spreadsheets/d/1X9aNeRnxxJbb_TAJurWqvf6Frrku4ffU78RrNdt_PN4/edit |

---

## 📌 Problem Statement

Indian admission processes suffer from:
- Applicants submitting incomplete or inconsistent academic records
- No awareness of India-specific education paths (Diploma, Lateral Entry, ITI)
- Zero work experience capture for professional programs
- Manual data entry into spreadsheets — slow, error-prone, unscalable
- No intelligence layer to flag risky or fraudulent applications

AdmitGuard V2 solves all of this with a 4-layer automated pipeline.

---

## 🏗️ System Architecture
```
┌─────────────────┐     JSON      ┌─────────────────┐
│   Frontend      │ ────────────▶ │   Backend API   │
│  (GitHub Pages) │               │   (Render)      │
└─────────────────┘               └────────┬────────┘
                                           │
                          ┌────────────────┼────────────────┐
                          ▼                ▼                 ▼
                   ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
                   │ Validation  │ │Intelligence │ │Google Sheets │
                   │ Engine      │ │ Layer       │ │(Persistent   │
                   │(Tier 1 & 2) │ │(Risk Score) │ │ Storage)     │
                   └─────────────┘ └─────────────┘ └──────────────┘
```

---

## 🧰 Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | HTML + CSS + JavaScript | Lightweight, no framework needed, deploys on GitHub Pages |
| Backend | Python Flask | Simple REST API, minimal setup, easy Render deployment |
| Storage | Google Sheets via gspread | Real-time, stakeholder-visible without any extra tools |
| Deployment (Frontend) | GitHub Pages + GitHub Actions | Free, auto-deploys on every push |
| Deployment (Backend) | Render (Free tier) | Simple Python hosting, supports environment variables |
| Intelligence | Rule-based weighted scoring | Fully explainable, no black box |

---

## ✨ Features

### 1. 🎓 Dynamic Education Path Handling
Supports all Indian education pathways — the form adapts in real time based on selection:
- **Path A — Standard:** 10th → 12th → UG → PG
- **Path B — Diploma:** 10th → Diploma → UG
- **Path C — Lateral Entry:** 10th → ITI → Diploma → UG

Per education level captures: Board/University, Stream, Year of Passing, Score (with scale — %, CGPA/10, CGPA/4), Backlogs, and Gap after level.

### 2. 💼 Work Experience Module
Captures complete professional history:
- Company, Designation, Domain, Employment Type
- Start/End dates with dynamic tenure calculation
- Key skills used
- Auto-computes: total experience, experience bucket, career gaps

### 3. ✅ Two-Tier Server-Side Validation Engine

**Tier 1 — Hard Reject** (data not saved):
- Missing mandatory fields
- Age below 18
- Chronologically impossible education years
- Score values outside valid range
- Education path violations (e.g. missing 12th for Path A)

**Tier 2 — Soft Flag** (saved but flagged for review):
- Education gap exceeding 24 months
- Active backlogs at any level
- Career gap between jobs exceeding 6 months
- No work experience but 3+ years since graduation

### 4. 🧠 Intelligence Layer

**Risk Scoring (0–100):**
| Factor | Impact |
|--------|--------|
| Education gap > 24 months | -15 points |
| Education gap > 12 months | -8 points |
| Each backlog | -5 points (max -20) |
| Declining academic trend | -10 points |
| Career gap > 6 months | -10 points |
| Multiple domain switches | -8 points |
| 2+ years experience | +10 points |
| 5+ years experience | +15 points |
| Improving academic trend | +5 points |

**Auto-Categorization:**
- 🟢 75–100 → Strong Fit
- 🟡 50–74 → Needs Review
- 🔴 0–49 → Weak Fit

**Experience Bucket:** Fresher / Junior (0-2yr) / Mid (2-5yr) / Senior (5+yr)

### 5. 📊 Real-Time Google Sheets Integration
Every validated application is automatically written to a shared Google Sheet with:
- All captured fields + all derived/computed fields
- Risk score and category
- Submission timestamp
- Validation status (Clean / Flagged)

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- pip
- A Google Cloud account (free)

### Steps

1. **Clone the repo**
```bash
git clone https://github.com/aditi23garg/admitguard-v2.git
cd admitguard-v2
```

2. **Set up backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Add environment variables**
Create a `.env` file inside `backend/`:
```
GOOGLE_CREDENTIALS_PATH=credentials.json
SHEET_ID=your_google_sheet_id_here
```

4. **Add Google credentials**
- Download `credentials.json` from Google Cloud (see setup guide below)
- Place it inside the `backend/` folder

5. **Run the backend**
```bash
python app.py
```
Backend runs at `http://localhost:5000`

6. **Open the frontend**
- Open `index.html` directly in your browser
- Or use Live Server in VS Code

---

## ☁️ Google Cloud Setup (One-time)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project → Enable **Google Sheets API** and **Google Drive API**
3. Go to **IAM & Admin → Service Accounts** → Create a service account
4. Download the JSON key → rename to `credentials.json`
5. Share your Google Sheet with the service account email as **Editor**
6. Copy the Sheet ID from the URL and add to `.env`

---

## 📁 Project Structure
```
admitguard-v2/
├── index.html              # Frontend — dynamic admission form
├── style.css               # Styling
├── script.js               # Form logic + API calls
├── backend/
│   ├── app.py              # Flask API — main entry point
│   ├── validation.py       # Tier 1 + Tier 2 validation rules
│   ├── intelligence.py     # Risk scoring + categorization
│   ├── sheets.py           # Google Sheets integration
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variable template
├── .github/
│   └── workflows/
│       └── pages.yml       # GitHub Actions auto-deployment
├── .gitignore
└── README.md
```

---

## 🧪 Test Scenarios

| # | Scenario | Expected Result |
|---|----------|----------------|
| 1 | Valid Path A application, no issues | ✅ Accepted, score shown, row in Sheet |
| 2 | Missing name and email | ❌ Rejected with field-level errors |
| 3 | 12th year before 10th year | ❌ Rejected — chronology violation |
| 4 | Path B (Diploma), 40-month gap | ✅ Accepted but flagged |
| 5 | Path C, 5 years experience, career gap | ✅ Accepted, high score, experience bucket shown |

---

## 🙋 Author

**Aditi Garg**
IITGN AI/ML Cohort 1 — Sprint 01
Built as part of AdmitGuard V2 sprint challenge
