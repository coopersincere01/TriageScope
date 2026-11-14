import os
from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
    """Display the TriageScope incident intake page."""
    return render_template("index.html")


@app.get("/health")
def health():
    """Provide a simple health check for deployment."""
    return {"status": "ok", "application": "TriageScope"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)