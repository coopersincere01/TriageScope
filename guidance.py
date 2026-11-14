"""Educational incident explanations and first-response guidance."""

PRIORITY_EXPLANATIONS = {
    "Low": (
        "The reported incident has a relatively low initial "
        "impact score. It still requires review because a low "
        "rating does not mean the incident is harmless."
    ),
    "Medium": (
        "The reported incident has a moderate initial impact "
        "score. Timely investigation is recommended to determine "
        "whether the situation is spreading or becoming more serious."
    ),
    "High": (
        "The reported incident has a high initial impact score. "
        "Prompt escalation and investigation are recommended "
        "because the reported circumstances could create "
        "significant operational or security consequences."
    ),
}

INCIDENT_ACTIONS = {
    "phishing": (
        "Preserve the suspicious email and its headers. "
        "Avoid opening attachments or following suspicious links."
    ),
    "malware": (
        "Collect relevant endpoint alerts and logs. "
        "Follow approved procedures before isolating affected devices."
    ),
    "unauthorized_access": (
        "Review authentication logs and affected accounts "
        "for evidence of unauthorized activity."
    ),
}


def build_explanation(incident, priority):
    """Explain the rating using the reported incident details."""

    explanation = PRIORITY_EXPLANATIONS[priority]
    contributing_factors = []

    if incident["system_importance"] == "high":
        contributing_factors.append(
            "the affected system is considered highly important"
        )

    if incident["affected_users"] == "multiple":
        contributing_factors.append(
            "multiple users may be affected"
        )

    if incident["sensitive_data"] == "yes":
        contributing_factors.append(
            "sensitive information may be involved"
        )

    if incident["incident_type"] == "unauthorized_access":
        contributing_factors.append(
            "possible unauthorized access was reported"
        )

    if contributing_factors:
        explanation += (
            " Factors requiring attention include "
            + "; ".join(contributing_factors)
            + "."
        )

    return explanation


def build_checklist(incident, priority):
    """Create an initial checklist tailored to the incident."""

    checklist = []

    if priority == "High":
        checklist.append(
            "Escalate promptly to the designated incident "
            "response or security team."
        )
    elif priority == "Medium":
        checklist.append(
            "Notify the security team and arrange timely triage."
        )
    else:
        checklist.append(
            "Record the report and schedule an initial security review."
        )

    checklist.append(
        "Preserve available evidence, including relevant "
        "timestamps, alerts, and logs."
    )

    checklist.append(
        INCIDENT_ACTIONS[incident["incident_type"]]
    )

    if incident["sensitive_data"] == "yes":
        checklist.append(
            "Identify potentially exposed sensitive information "
            "and follow applicable notification procedures."
        )

    if incident["affected_users"] == "multiple":
        checklist.append(
            "Determine the number of affected users "
            "and whether additional systems are involved."
        )

    checklist.append(
        "Document findings, follow approved incident response "
        "procedures, and reassess the priority as new evidence appears."
    )

    return checklist