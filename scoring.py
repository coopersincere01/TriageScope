"""Rule-based incident priority assessment for TriageScope."""

SCORING_RULES = {
    "incident_type": {
        "phishing": 0,
        "malware": 1,
        "unauthorized_access": 2,
    },
    "system_importance": {
        "low": 0,
        "medium": 2,
        "high": 4,
    },
    "affected_users": {
        "one": 0,
        "multiple": 2,
    },
    "sensitive_data": {
        "no": 0,
        "yes": 4,
    },
}


def calculate_priority(incident):
    """Return the priority, score, and contributing factors."""

    factors = []
    total_score = 0

    for field, options in SCORING_RULES.items():
        value = incident.get(field)

        if value not in options:
            raise ValueError(
                f"Missing or invalid value for {field}"
            )

        points = options[value]
        total_score += points

        factors.append({
            "field": field,
            "selection": value,
            "points": points,
        })

    if total_score >= 6:
        priority = "High"
    elif total_score >= 3:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "priority": priority,
        "score": total_score,
        "max_score": 12,
        "factors": factors,
    }