import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime

def write_to_sheet(data, flags, score_data):
    creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    sheet_id = os.getenv("SHEET_ID")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1

    # Summarize education
    edu_summary = " | ".join([
        f"{e['level']}: {e.get('score','?')} ({e.get('scoreScale','?')}) [{e.get('yearOfPassing','?')}]"
        for e in data.get("education", []) if e.get("board")
    ])

    # Summarize work
    work_summary = " | ".join([
        f"{j.get('company','?')} ({j.get('domain','?')}, {j.get('employmentType','?')}) {j.get('startDate','')}–{j.get('endDate','')}"
        for j in data.get("workExperience", [])
    ])

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("dob", ""),
        data.get("educationPath", ""),
        edu_summary,
        work_summary,
        score_data.get("risk_score", ""),
        score_data.get("category", ""),
        score_data.get("experience_bucket", ""),
        score_data.get("total_experience_months", ""),
        "; ".join(flags) if flags else "None",
        "Flagged" if flags else "Clean"
    ]

    sheet.append_row(row)
