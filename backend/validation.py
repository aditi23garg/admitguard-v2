from datetime import datetime

LEVEL_ORDER = {
    "10th": 1, "ITI": 2, "12th": 2,
    "Diploma": 3, "UG": 4, "PG": 5, "PhD": 6
}

def validate_application(data):
    tier1 = []
    tier2 = []

    # ── TIER 1: HARD REJECT ─────────────────────────────────

    # Mandatory personal fields
    if not data.get("name", "").strip():
        tier1.append({"field": "name", "message": "Full name is required"})
    if not data.get("email", "").strip():
        tier1.append({"field": "email", "message": "Email address is required"})
    if not data.get("phone", "").strip():
        tier1.append({"field": "phone", "message": "Phone number is required"})
    if not data.get("dob", "").strip():
        tier1.append({"field": "dob", "message": "Date of birth is required"})

    # Age check
    dob = data.get("dob", "")
    if dob:
        try:
            age = calculate_age(dob)
            if age < 18:
                tier1.append({"field": "dob", "message": f"Applicant is {age} years old — must be at least 18"})
        except:
            tier1.append({"field": "dob", "message": "Invalid date of birth format"})

    # Education path must be selected
    path = data.get("educationPath")
    if not path:
        tier1.append({"field": "path", "message": "Education path must be selected"})

    education = data.get("education", [])

    # 10th is mandatory for all paths
    levels_present = [e["level"] for e in education if e.get("board")]
    if "10th" not in levels_present:
        tier1.append({"field": "education", "message": "10th grade details are mandatory for all paths"})

    # Path A: 12th mandatory
    if path == "A":
        if "UG" in levels_present and "12th" not in levels_present:
            tier1.append({"field": "education", "message": "Path A requires 12th details before UG"})

    # Path B: Diploma mandatory
    if path == "B":
        if "Diploma" not in levels_present:
            tier1.append({"field": "education", "message": "Path B (Diploma route) requires Diploma details"})

    # Chronological year check
    filled = [e for e in education if e.get("yearOfPassing") and e.get("board")]
    filled_sorted = sorted(filled, key=lambda x: LEVEL_ORDER.get(x["level"], 99))
    years = [e["yearOfPassing"] for e in filled_sorted]
    for i in range(1, len(years)):
        if years[i] < years[i-1]:
            tier1.append({
                "field": "education",
                "message": f"Year of passing must increase across education levels — check {filled_sorted[i]['level']}"
            })
            break

    # Score range check + future year check
    current_year = datetime.now().year
    for entry in education:
        if not entry.get("board"):
            continue
        score = entry.get("score")
        scale = entry.get("scoreScale", "percentage")
        yr = entry.get("yearOfPassing")

        if yr and yr > current_year:
            tier1.append({"field": "education", "message": f"Year of passing for {entry['level']} cannot be in the future"})

        if score is not None:
            if scale == "percentage" and (score < 0 or score > 100):
                tier1.append({"field": "education", "message": f"Percentage score for {entry['level']} must be between 0 and 100"})
            if scale == "cgpa10" and (score < 0 or score > 10):
                tier1.append({"field": "education", "message": f"CGPA (10-pt) for {entry['level']} must be between 0 and 10"})
            if scale == "cgpa4" and (score < 0 or score > 4):
                tier1.append({"field": "education", "message": f"CGPA (4-pt) for {entry['level']} must be between 0 and 4"})

    # Work experience: end date after start date
    for job in data.get("workExperience", []):
        start = job.get("startDate", "")
        end = job.get("endDate", "")
        if start and end and end != "Present":
            if end < start:
                tier1.append({
                    "field": "work",
                    "message": f"End date for {job.get('company', 'a job')} cannot be before start date"
                })

    # ── TIER 2: SOFT FLAGS ──────────────────────────────────

    # Total education gap > 24 months
    total_gap = sum(e.get("gapAfter", 0) for e in education)
    if total_gap > 24:
        tier2.append(f"Total education gap is {total_gap} months (exceeds 24 months) — flagged for review")

    # Any backlogs
    for entry in education:
        if entry.get("backlogs", 0) > 0:
            tier2.append(f"Active backlogs in {entry['level']}: {entry['backlogs']} — flagged for review")

    # Career gaps > 6 months
    work = data.get("workExperience", [])
    sorted_work = sorted(work, key=lambda x: x.get("startDate", ""))
    for i in range(1, len(sorted_work)):
        prev_end = sorted_work[i-1].get("endDate", "")
        curr_start = sorted_work[i].get("startDate", "")
        if prev_end and curr_start and prev_end != "Present":
            gap = months_between(prev_end, curr_start)
            if gap > 6:
                tier2.append(f"Career gap of {gap} months between jobs — flagged for review")

    # No work experience but 3+ years since last education
    if not work:
        last_years = [e.get("yearOfPassing") for e in education if e.get("yearOfPassing")]
        if last_years:
            years_since = datetime.now().year - max(last_years)
            if years_since >= 3:
                tier2.append(f"No work experience declared but {years_since} years since last education — flagged for review")

    return {"tier1": tier1, "tier2": tier2}


def calculate_age(dob_str):
    dob = datetime.strptime(dob_str, "%Y-%m-%d")
    today = datetime.today()
    return (today - dob).days // 365


def months_between(d1_str, d2_str):
    try:
        d1 = datetime.strptime(d1_str, "%Y-%m")
        d2 = datetime.strptime(d2_str, "%Y-%m")
        return max(0, (d2.year - d1.year) * 12 + d2.month - d1.month)
    except:
        return 0