def score_job(job: dict) -> dict:
    """
    Score a job posting based on experience, clearance requirements,
    seniority level, and cybersecurity/networking keyword matches.
    """

    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    combined_text = f"{title} {description}"

    score = 0
    reasons = []

    strong_keywords = [
        "soc",
        "siem",
        "security operations",
        "incident response",
        "alert triage",
        "network security",
        "network traffic",
        "detection",
        "detections",
        "splunk",
        "firewall",
        "ids",
        "ips",
        "phishing",
        "vulnerability",
        "log analysis",
        "endpoint detection",
        "edr",
    ]

    clearance_keywords = [
        "active secret",
        "active top secret",
        "top secret",
        "ts/sci",
        "sci clearance",
        "polygraph",
        "security clearance required",
        "current clearance",
        "must possess a clearance",
        "must have a clearance",
        "dod clearance",
    ]

    senior_keywords = [
        "senior",
        "lead",
        "principal",
        "architect",
        "manager",
        "7+ years",
        "8+ years",
        "10+ years",
    ]

    entry_mid_keywords = [
        "entry level",
        "junior",
        "associate",
        "1+ year",
        "1 year",
        "2+ years",
        "2 years",
        "3+ years",
        "3 years",
    ]

    # Hard reject if active clearance is required
    for keyword in clearance_keywords:
        if keyword in combined_text:
            return {
                **job,
                "fit_score": 0,
                "decision": "Reject",
                "reasons": [f"Reject: clearance requirement detected: {keyword}"],
            }

    # Add points for strong cybersecurity/networking alignment
    for keyword in strong_keywords:
        if keyword in combined_text:
            score += 10
            reasons.append(f"Matched relevant keyword: {keyword}")

    # Add points for entry/mid-level experience language
    for keyword in entry_mid_keywords:
        if keyword in combined_text:
            score += 10
            reasons.append(f"Good experience-level signal: {keyword}")

    # Subtract points for seniority signals
    for keyword in senior_keywords:
        if keyword in combined_text:
            score -= 25
            reasons.append(f"Possible senior-level signal: {keyword}")

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    # Decide recommendation
    if score >= 70:
        decision = "Apply"
    elif score >= 45:
        decision = "Maybe"
    elif score == 0:
        decision = "Reject"
    else:
        decision = "Skip"

    return {
        **job,
        "fit_score": score,
        "decision": decision,
        "reasons": reasons,
    }