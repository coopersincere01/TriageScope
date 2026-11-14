import os
from flask import Flask, render_template, request
from scoring import calculate_priority
from guidance import build_explanation, build_checklist

app = Flask(__name__)

# Allowed incident intake values
ALLOWED_VALUES = {
    "incident_type": {
        "phishing", "malware", "unauthorized_access"
    },
    "system_importance": {
        "low", "medium", "high"
    },
    "affected_users": {
        "one", "multiple"
    },
    "sensitive_data": {
        "yes", "no"
    }
}

FIELD_LABELS = {
    "incident_type": "Incident Type",
    "system_importance": "System Importance",
    "affected_users": "Number of Affected Users",
    "sensitive_data": "Sensitive Information"
}


@app.route("/", methods=["GET", "POST"])
def index():
    """Validate incident details and calculate an initial priority."""

    errors = []
    form_values = {}
    submitted = False
    result = None

    if request.method == "POST":

        for field, allowed in ALLOWED_VALUES.items():
            value = request.form.get(field, "").strip()
            form_values[field] = value

            if not value:
                errors.append(
                    f"{FIELD_LABELS[field]} is required."
                )
            elif value not in allowed:
                errors.append(
                    f"Invalid selection for {FIELD_LABELS[field]}."
                )

        if not errors:
            result = calculate_priority(form_values)
            submitted = True

            result["explanation"] = build_explanation(
                form_values, result["priority"]
            )
            result["checklist"] = build_checklist(
                form_values, result["priority"]
            )

    return render_template(
        "index.html",
        errors=errors,
        submitted=submitted,
        form_values=form_values,
        result=result,
        field_labels=FIELD_LABELS
    ), 400 if errors else 200


@app.get("/health")
def health():
    """Health check for Docker and cloud deployment."""
    return {
        "status": "ok",
        "application": "TriageScope"
    }, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)