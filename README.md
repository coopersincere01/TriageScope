# TriageScope
### Cyber Incident Priority Assistant

## Project Overview

TriageScope is a web application I am developing to help cybersecurity students and entry-level analysts practice assessing security incidents. Not every incident has the same level of risk, and understanding which situations need attention first is an important part of incident response.

I chose this project because it connects my interests in cybersecurity, incident response, and business impact. I wanted to create something useful without making the application unnecessarily complicated.

TriageScope will help users review incident details, identify an initial priority level, and understand what factors influenced the assessment. The application is intended as a learning tool and will not replace an analyst's judgment or an organization's incident response procedures.

## Planned Features

The application will include four main features:

1. **Incident Intake Form:** Users can enter details about a security incident, including the incident type, system importance, affected users, and whether sensitive information may be involved.

2. **Priority Assessment:** The application will use predefined rules to assign a Low, Medium, or High priority rating.

3. **Priority Explanation:** Users will receive an explanation of the factors that contributed to the rating.

4. **Response Checklist:** The application will provide recommended first-response actions based on the incident type and priority level.

I also plan to add sample incident scenarios and a Clear Form option in the final version.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | SQLite |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |
| Automated Testing | Pytest |
| CI/CD | GitHub Actions |
| Cloud Deployment | Google Cloud Run |
| AI-Assisted Coding | GitHub Copilot |
| Project Management | Jira |
| Project Documentation | Confluence |

I selected this technology stack because it supports the course requirements while keeping the application manageable. Flask provides a straightforward way to develop the backend, while Docker will help the application run consistently across different environments.

## How the Application Will Work

TriageScope will follow a straightforward assessment process:

1. Users enter cybersecurity incident details through the intake form.
2. The Flask backend validates the submitted information.
3. The application evaluates the incident using predefined scoring rules.
4. Users receive a Low, Medium, or High priority rating.
5. The results include an explanation and recommended first-response checklist.

SQLite will be used to store sample incident scenarios and response templates. The application will not require user accounts or store actual company incident reports.

## Installation and Setup

TriageScope is currently in the planning stage. Installation instructions will be updated as the application is developed.

The planned setup process includes:

1. Clone the GitHub repository.
2. Install the required Python dependencies.
3. Configure the Flask application.
4. Build and run the application using Docker Compose.
5. Access the application through a local web browser.

Once the MVP is complete, this section will include the exact installation commands, required dependencies, configuration settings, and troubleshooting instructions.

## AI-Assisted Development

I plan to use GitHub Copilot to assist with code generation, debugging, and application development.

AI assistance has also been used during the planning process to help organize project requirements, develop user stories, and structure development tasks.

During development, I will document specific examples of AI-assisted code, how the suggestions were tested, and any modifications made before including them in the application.

AI-generated code will be reviewed and tested to ensure it meets the application's requirements.

## Development Timeline

### Sprint 1: MVP Development
**November 9–22, 2026**

Focus on building the core functionality of TriageScope, including:

- Incident intake form
- Rule-based priority assessment
- Priority explanations
- Recommended response checklist
- Docker and Docker Compose configuration
- Initial Google Cloud Run deployment

### Sprint 2: Automated Testing and CI/CD
**November 23–December 6, 2026**

Focus on improving application reliability and automating development workflows.

- Develop automated tests using Pytest
- Configure GitHub Actions
- Run tests when code changes are submitted
- Prevent deployment when tests fail
- Automate successful deployments to Google Cloud Run

### Sprint 3: Final Improvements
**December 7–13, 2026**

Focus on completing the application and preparing it for final submission.

- Add sample cybersecurity incident scenarios
- Implement the Clear Form feature
- Improve the interface and user experience
- Resolve remaining issues
- Complete project documentation
- Verify the final cloud deployment

## Project Management

### Jira

I am using Jira to organize the project into three epics and nine user stories. Each story includes acceptance criteria, story points, and development subtasks.

The work is organized into three sprints that align with the course deadlines.

**Jira Project:** [TriageScope Jira Backlog](https://sinceresworkspace-42429653.atlassian.net/jira/software/projects/TRIAGE/boards/2/backlog)

### Confluence

Confluence will be used to document project planning, technical decisions, development progress, and challenges encountered.

Sprint reviews and retrospectives will also be documented to reflect what was accomplished, what needs improvement, and any changes made during development.

### GitHub

GitHub will be used for version control and maintaining the application code.

Development will include feature branches, descriptive commit messages, and pull requests to organize and review changes before merging them into the main branch.

## Current Project Status

**Planning and Design — Unit 11**

The project concept, technology stack, user stories, and sprint plan have been established.

The next phase will focus on developing the MVP, configuring Docker, and attempting the initial deployment to Google Cloud Run.

This README will be updated as application features are developed, tested, and deployed.
