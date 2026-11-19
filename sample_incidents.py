"""Fictional practice scenarios for TriageScope."""

SAMPLE_INCIDENTS = [
    {
        "id": "suspicious-email",
        "title": "Suspicious Email",
        "description": "One person receives a suspicious email on a low-importance system.",
        "fields": {
            "incident_type": "phishing",
            "system_importance": "low",
            "affected_users": "one",
            "sensitive_data": "no",
        },
    },
    {
        "id": "workstation-malware",
        "title": "Malware on Workstations",
        "description": "Malware affects multiple users on systems of medium importance.",
        "fields": {
            "incident_type": "malware",
            "system_importance": "medium",
            "affected_users": "multiple",
            "sensitive_data": "no",
        },
    },
    {
        "id": "unauthorized-access",
        "title": "Unauthorized Access",
        "description": "Multiple users are affected by unauthorized access to a critical system containing sensitive information.",
        "fields": {
            "incident_type": "unauthorized_access",
            "system_importance": "high",
            "affected_users": "multiple",
            "sensitive_data": "yes",
        },
    },
]

SAMPLES_BY_ID = {
    sample["id"]: sample for sample in SAMPLE_INCIDENTS
}
