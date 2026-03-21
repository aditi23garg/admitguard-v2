from datetime import datetime

def score_application(data):
    score = 100
    reasons = []

    education = data.get("education", [])
    work = data.get("workExperience", [])

    # 1. Education gap penalty
    total_gap = sum(e.get("gapAfter", 0) for e in education)
    if total_gap > 24:
        score -= 15
        reasons.append(f"Large education gap ({total_gap} months): -15")
    elif total_gap > 12:
        score -= 8
        reasons.append(f"Moderate education gap ({total_gap} months): -8")

    # 2. Backlog penalty (max -20)
    total_backlogs = sum(e.get("backlogs", 0) for e in education)
    deduction = min(total_backlogs * 5, 20)
    if deduction > 0:
        score -= deduction
        reasons.append(f"Backlogs ({total_backlogs} total): -{deduction}")

    # 3. Score trend — is academic performance improving?
    normalized = [normalize_score(e) for e in education if e.get("score") is not None]
    if len(normalized) >= 2:
        if normalized[-1] < normalized[0] - 10:
            score -= 10
            reasons.append("Declining academic performance trend: -10")
        elif normalized[-1] > normalized[0] + 5:
            score += 5
            reasons.append("Improving academic performance trend: +5")

    # 4. Work experience bonus
    total_months = calculate_total_experience(work)
    if total_months >= 60:
        score += 15
        reasons.append(f"Senior experience ({total_months} months): +15")
    elif total_months >= 24:
        score += 10
        reasons.append(f"Mid-level experience ({total_months} months): +10")
    elif total_months >= 6:
        score += 5
        reasons.append(f"Some experience ({total_months} months): +5")

    # 5. Career gap penalty
    career_gaps = get_career_gaps(work)
    if any(g > 6 for g in career_gaps):
        score -= 10
        reasons.append("Career gap > 6 months detected: -10")

    # 6. Too many domain switches (> 3 different domains)
    domains = list(set(j.get("domain", "") for j in work if j.get("domain")))
    if len(domains) > 3:
        score -= 8
        reasons.append(f"Multiple domain switches ({len(domains)} domains): -8")

    # Clamp
    score = max(0, min(100, score))

    # Category
    if score >= 75:
        category = "Strong Fit"
    elif score >= 50:
        category = "Needs Review"
    else:
        category = "Weak Fit"

    # Experience bucket
    if total_months == 0:
        bucket = "Fresher"
    elif total_months <= 24:
        bucket = "Junior (0-2yr)"
    elif total_months <= 60:
        bucket = "Mid (2-5yr)"
    else:
        bucket = "Senior (5+yr)"

    return {
        "risk_score": score,
        "category": category,
        "experience_bucket": bucket,
        "total_experience_months": total_months,
        "score_breakdown": reasons
    }


def normalize_score(entry):
    score = float(entry.get("score", 0))
    scale = entry.get("scoreScale", "percentage")
    if scale == "cgpa10":
        return score * 9.5
    elif scale == "cgpa4":
        if score >= 3.7: return 90
        elif score >= 3.3: return 85
        elif score >= 3.0: return 80
        elif score >= 2.7: return 75
        else: return 60
    return score


def calculate_total_experience(work):
    total = 0
    for job in work:
        start = job.get("startDate", "")
        end = job.get("endDate", "")
        if not start:
            continue
        if end == "Present" or not end:
            end = datetime.now().strftime("%Y-%m")
        total += months_between(start, end)
    return total


def get_career_gaps(work):
    gaps = []
    sorted_work = sorted(work, key=lambda x: x.get("startDate", ""))
    for i in range(1, len(sorted_work)):
        prev_end = sorted_work[i-1].get("endDate", "")
        curr_start = sorted_work[i].get("startDate", "")
        if prev_end and prev_end != "Present" and curr_start:
            gap = months_between(prev_end, curr_start)
            if gap > 0:
                gaps.append(gap)
    return gaps


def months_between(d1_str, d2_str):
    try:
        d1 = datetime.strptime(d1_str, "%Y-%m")
        d2 = datetime.strptime(d2_str, "%Y-%m")
        return max(0, (d2.year - d1.year) * 12 + d2.month - d1.month)
    except:
        return 0
