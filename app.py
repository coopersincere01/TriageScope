import os
from flask import Flask, render_template, request
from scoring import calculate_priority
from guidance import build_explanation, build_checklist
from sample_incidents import SAMPLE_INCIDENTS, SAMPLES_BY_ID

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

    if request.method == "GET":
        sample = SAMPLES_BY_ID.get(request.args.get("sample", ""))
        if sample:
            form_values = sample["fields"].copy()

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
        sample_incidents=SAMPLE_INCIDENTS,
        field_labels=FIELD_LABELS
    ), 400 if errors else 200



@app.route("/compare", methods=["GET", "POST"])
def compare_incidents():
    """Compare two incident assessments using the existing rules."""

    errors = []
    incident_values = {"a": {}, "b": {}}
    comparisons = None
    winner = None

    if request.method == "POST":
        for incident_id in ("a", "b"):
            for field, allowed in ALLOWED_VALUES.items():
                value = request.form.get(
                    f"{incident_id}_{field}", ""
                ).strip()
                incident_values[incident_id][field] = value

                if not value:
                    errors.append(
                        f"Incident {incident_id.upper()}: "
                        f"{FIELD_LABELS[field]} is required."
                    )
                elif value not in allowed:
                    errors.append(
                        f"Incident {incident_id.upper()}: "
                        f"Invalid selection for {FIELD_LABELS[field]}."
                    )

        if not errors:
            comparisons = {
                incident_id: calculate_priority(incident_values[incident_id])
                for incident_id in ("a", "b")
            }

            a_score = comparisons["a"]["score"]
            b_score = comparisons["b"]["score"]

            if a_score > b_score:
                winner = "Incident A has the higher assessment score."
            elif b_score > a_score:
                winner = "Incident B has the higher assessment score."
            else:
                winner = "Both incidents have the same assessment score."

    return render_template(
        "compare.html",
        errors=errors,
        incident_values=incident_values,
        comparisons=comparisons,
        winner=winner
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