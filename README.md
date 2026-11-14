# TriageScope
### Cyber Incident Priority Assistant

**Status:** MVP Complete — November 2026

**Live Application:** https://triagescope-168374564156.us-central1.run.app

**GitHub Repository:** https://github.com/coopersincere01/TriageScope

## Project Overview

TriageScope is a web application I created to help cybersecurity students and entry-level analysts practice assessing security incidents. Not every incident has the same level of risk, and knowing what needs attention first is an important part of incident response.

I chose this project because it connects my interests in cybersecurity, incident response, and business impact. I wanted to build something practical that explains why an incident might be more serious than another without making the application unnecessarily complicated.

Users enter basic incident details, and TriageScope assigns an initial Low, Medium, or High priority. The application also explains the rating and provides a recommended first-response checklist.

TriageScope is intended for learning and practice. It does not replace an analyst's judgment or an organization's incident response procedures.

## Features

The MVP includes four main features:

1. **Incident Intake Form:** Users select an incident type, system importance, number of affected users, and whether sensitive information may be involved. The application validates the information before processing it.

2. **Priority Assessment:** TriageScope uses predefined scoring rules to calculate a Low, Medium, or High priority rating.

3. **Priority Explanation:** The results explain what the rating means and identify the incident characteristics that influenced the assessment.

4. **Response Checklist:** Users receive recommended initial response actions based on their incident details and priority level.

The application preserves the selected form values after an assessment and displays validation errors when necessary.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, Jinja2 |
| Backend | Python, Flask |
| Production Web Server | Gunicorn |
| Containerization | Docker, Docker Compose |
| Automated Testing | Python unittest |
| Version Control | Git, GitHub |
| Cloud Deployment | Google Cloud Run |
| Project Management | Jira |
| Documentation | Confluence |

I selected these technologies because they meet the course requirements while keeping the application manageable.

The current MVP does not require a database or user accounts. Additional features, including sample incidents and CI/CD, are planned for later development.

## How TriageScope Works

The assessment process follows these steps:

1. The user enters the incident details through the website.
2. Flask checks that all required fields contain valid selections.
3. The scoring module calculates a numerical incident score.
4. The application assigns a Low, Medium, or High priority.
5. The guidance module generates an explanation and response checklist.
6. The completed assessment appears on the website.

### Scoring Rules

| Incident Factor | Selection | Points |
|---|---|---:|
| Incident Type | Phishing | 0 |
| Incident Type | Malware | 1 |
| Incident Type | Unauthorized Access | 2 |
| System Importance | Low | 0 |
| System Importance | Medium | 2 |
| System Importance | High | 4 |
| Affected Users | One | 0 |
| Affected Users | Multiple | 2 |
| Sensitive Information | No | 0 |
| Sensitive Information | Yes | 4 |

The total score determines the priority:

| Score | Priority |
|---|---|
| 0–2 | Low |
| 3–5 | Medium |
| 6–12 | High |

These scoring rules were developed specifically for this educational project. They are not an official cybersecurity severity standard.

For example, an incident involving unauthorized access to a highly important system, multiple affected users, and sensitive information receives a score of **12/12 — High Priority**.

## Installation and Local Setup

### Requirements

- Python 3.12 or a compatible Python 3 version
- Git
- pip
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/coopersincere01/TriageScope.git
cd TriageScope
```

### 2. Create a Virtual Environment

For Linux or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

This starts Flask's development server. The deployed application uses Gunicorn instead.

## Running TriageScope with Docker

Docker allows the application to run in a consistent environment without manually setting up its Python dependencies.

### Requirements

- Docker
- Docker Compose

### Build and Start

From the project directory, run:

```bash
docker compose up --build -d
```

Once the container starts, open:

http://localhost:5001

Docker Compose maps port 5001 on the local machine to port 8080 inside the container.

### Check the Container

```bash
docker compose ps
```

The container should report a healthy status.

### Test the Health Endpoint

```bash
curl http://127.0.0.1:5001/health
```

Expected response:

```json
{"application":"TriageScope","status":"ok"}
```

### View Logs

```bash
docker compose logs
```

### Stop the Container

```bash
docker compose down
```

The Dockerfile uses Python 3.12, installs the required dependencies, and runs the application through Gunicorn as a non-root user.

The container also supports the `PORT` environment variable required for Google Cloud Run.

## Google Cloud Deployment

TriageScope was successfully deployed to Google Cloud Run during MVP development.

**Project ID:** `triagescope`

**Service:** `triagescope`

**Region:** `us-central1`

**Live Website:** https://triagescope-168374564156.us-central1.run.app

### Deployment Process

I used Google Cloud Shell to clone the GitHub repository and deploy the application using its Dockerfile.

The deployment command was:

```bash
gcloud run deploy triagescope \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --min-instances 0 \
  --max-instances 2
```

Google Cloud required the Cloud Run, Cloud Build, and Artifact Registry services.

The first deployment attempt failed because the default service account did not have the required permissions. After assigning the Cloud Run Builder role (`roles/run.builder`) to the appropriate service account, the deployment succeeded.

I verified the public website using a private browser window and submitted a test incident to confirm that the priority calculation, explanation, and checklist were working correctly.

A $5 monthly billing budget alert was also configured for the project, with notifications at 50%, 90%, and 100%. These alerts provide spending notifications rather than a guaranteed spending limit.

## Testing

Automated testing was used throughout development to make sure new features worked without breaking existing functionality.

TriageScope uses Python's built-in `unittest` framework.

### Run the Tests

```bash
python -m unittest discover -s tests -v
```

### Verified Results

```text
Ran 20 tests

OK
```

The 20 automated tests cover:

- Homepage and health endpoint availability
- Valid and invalid incident submissions
- Required-field validation
- Low, Medium, and High scoring
- Consistent scoring results
- Invalid scoring inputs
- Priority results displayed on the website
- Priority explanations
- Incident-specific response checklists

I also manually tested the application in the browser, through Docker Compose, and on Google Cloud Run.

## Troubleshooting

### Port 5000 Is Already in Use

If Flask reports that port 5000 is already in use, another application process may still be running.

Stop the previous Flask server using `Ctrl+C` in its terminal before restarting the application.

### Website Changes Are Not Appearing

Make sure the edited files are saved.

Restart Flask after changing application code. If using Docker, rebuild the image with:

```bash
docker compose up --build -d
```

Refresh the browser after restarting the application.

### Docker Container Is Not Running

Check the container status and logs:

```bash
docker compose ps
docker compose logs
```

Review any reported errors before rebuilding the image.

### Python Cannot Find the Tests

Keep test files directly inside the `tests` directory, using filenames beginning with `test_`.

Run:

```bash
python -m unittest discover -s tests -v
```

### Google Cloud Deployment Permissions

If a Cloud Run source deployment reports missing service account permissions, verify that the account responsible for building the application has the required IAM permissions.

The MVP deployment issue was resolved by granting the Cloud Run Builder role to the project's default build service account.

Permissions should be limited to the roles actually required.

## AI-Assisted Development

I used ChatGPT during development to help organize implementation steps, draft portions of the Python code, troubleshoot errors, and develop automated tests.

I treated the suggestions as a starting point rather than assuming they would work correctly. I reviewed the results, tested the application, and made changes when something did not work as expected.

### Example 1: Priority Scoring

AI assistance helped develop the rule-based priority calculation in `scoring.py`.

One part of the scoring logic is:

```python
if total_score >= 6:
    priority = "High"
elif total_score >= 3:
    priority = "Medium"
else:
    priority = "Low"
```

I verified the calculations using automated tests for all three priority levels, invalid inputs, and consistent results.

### Example 2: Connecting the Backend to the Website

AI assistance helped integrate the scoring and guidance modules into the Flask application.

For example, `app.py` includes:

```python
result = calculate_priority(form_values)
result["explanation"] = build_explanation(
    form_values, result["priority"]
)
result["checklist"] = build_checklist(
    form_values, result["priority"]
)
```

During testing, the backend calculated the correct priority, but the website initially displayed only the old confirmation message. I checked the files, corrected the HTML integration, and verified that the assessment appeared correctly.

An earlier HTML replacement also changed the website's original appearance. I restored the original layout and kept the new functionality.

### Example 3: Docker

AI assistance helped create the Dockerfile and Docker Compose configuration.

I verified the configuration by building the Docker image, checking the container's health status, and submitting an incident through the containerized application.

These examples showed me why testing and reviewing AI-assisted code are important, especially when changes affect multiple parts of an application.

## Development Workflow and Project Management

### GitHub

I used feature branches, descriptive commits, and pull requests to organize development.

Four feature pull requests were completed and merged during the MVP:

1. Incident intake form and validation
2. Rule-based priority scoring
3. Priority explanations and response checklists
4. Docker and Docker Compose configuration

I tested each major feature before merging it into the main branch.

### Jira

I used Jira to organize development into user stories, subtasks, and three planned sprints.

**Jira Backlog:**
https://sinceresworkspace-42429653.atlassian.net/jira/software/projects/TRIAGE/boards/2/backlog

The main MVP stories include:

- TRIAGE-4 — Incident Intake Form
- TRIAGE-6 — Required-Field Validation
- TRIAGE-14 — Priority Assessment
- TRIAGE-17 — Priority Explanation
- TRIAGE-20 — Response Checklist
- TRIAGE-23 — Docker and Google Cloud Deployment

### Confluence

I used Confluence for project planning and documentation.

**Project Overview:**
https://sinceresworkspace-42429653.atlassian.net/wiki/spaces/TSCOPE/pages/65859/Project+Overview

## Development Timeline

### Sprint 1: MVP Development
**November 9–22, 2026**

Focus:

- Incident intake and validation
- Rule-based priority assessment
- Priority explanations
- Response checklists
- Docker configuration
- Google Cloud Run deployment

These core development tasks were completed and tested during the MVP.

### Sprint 2: Automated Testing and CI/CD
**November 23–December 6, 2026**

Planned improvements:

- Expand automated testing
- Add GitHub Actions
- Automate testing when changes are pushed
- Explore automated Cloud Run deployment

### Sprint 3: Final Improvements
**December 7–13, 2026**

Planned improvements:

- Add sample incident scenarios
- Implement a Clear Form option
- Improve the user experience
- Resolve remaining issues
- Complete final project documentation

## Current Status

The TriageScope MVP is developed, tested, containerized, and deployed.

Completed work includes four core application features, 20 passing automated tests, four merged feature pull requests, Docker Compose verification, and a working Google Cloud Run website.

The next phase will focus on CI/CD, additional functionality, and final refinements before the December 13 project deadline.

**Security Note:** TriageScope is an educational application. Users should not enter real company incident reports, passwords, or sensitive information.