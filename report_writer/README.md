### Repository Notes

This repository intentionally excludes auto-generated and local
environment files such as:

- Python virtual environments (`venv/`, `.venv/`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Editor configuration folders (e.g., `.vscode/`)
- OS-specific files (e.g., `.DS_Store`)
- Generated outputs (PDFs, images, logs)

These files are excluded via `.gitignore` to ensure the repository
contains only source code and configuration required to reproduce
results.
## Report Writer Agent — Student 3

This agent synthesizes market sentiment and quantitative metrics
into a structured financial report.

### Inputs
- Market Research Agent JSON
- Data Analyst Agent JSON

### Outputs
- Text-based financial report
- Ready for PDF or Streamlit integration

### Project Contribution Summary

I implemented the Report Writer Agent responsible for combining market
sentiment outputs and quantitative financial metrics into a structured
financial report. My contribution included defining the JSON schema for
agent communication, developing prompt templates to control analysis scope
and prevent hallucinated outputs, and implementing Python logic for input
validation and report generation. I also ensured clean documentation and
professional version control practices using a feature branch and pull
request workflow.

