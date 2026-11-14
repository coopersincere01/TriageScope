# Lightweight Python base image.
FROM python:3.12-slim

# Improve Python logging and disable bytecode files.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install dependencies before copying source for better caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application files needed to run TriageScope.
COPY app.py scoring.py guidance.py ./
COPY templates/ ./templates/
COPY static/ ./static/

# Run the application without root privileges.
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8080

# Gunicorn listens on the port supplied by Cloud Run.
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 2 --access-logfile - app:app"]
