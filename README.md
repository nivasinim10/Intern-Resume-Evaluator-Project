# Intern Resume Evaluator

A Streamlit-based Resume Screening Application that compares uploaded PDF resumes against a job or internship description and ranks candidates using text similarity, skill matching, and experience-based scoring.

This project helps reduce manual resume screening effort by automatically analyzing resumes, extracting candidate details, computing relevance scores, and ranking applicants through an interactive web interface.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Application Versions](#application-versions)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Application Workflow](#application-workflow)
- [How It Works](#how-it-works)
- [Sample Resume Files](#sample-resume-files)
- [Installation](#installation)
- [How to Run the Project](#how-to-run-the-project)
- [Output](#output)
- [Scoring Logic](#scoring-logic)
- [Core Functionalities](#core-functionalities)
- [Challenges Solved](#challenges-solved)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Academic Purpose](#academic-purpose)
- [Repository Goals](#repository-goals)
- [Author](#author)

---

# Project Overview

This project implements an AI-assisted Resume Evaluation and Candidate Ranking System using Streamlit.

The application allows recruiters or hiring teams to:

- Upload one or more PDF resumes
- Enter a job or internship description
- Compare resumes against job requirements
- Compute similarity and skill-based scores
- Rank candidates automatically
- Export filtered reports as CSV and Excel files

The system is designed to simulate a lightweight Applicant Tracking System (ATS) workflow for internship and entry-level recruitment.

---

# Features

## Resume Upload System

- Upload multiple PDF resumes
- Batch candidate processing
- PDF text extraction using `PyPDF2`
- Resume preprocessing and cleanup

---

## Candidate Information Extraction

The application extracts:

- Email address
- Phone number
- Degree keywords
- Skills
- Experience indicators
- Resume text content

---

## Resume Scoring

The system calculates:

- TF-IDF text similarity
- Skill match percentage
- Experience score
- Project relevance score *(app1.py)*
- Internship-aware ranking logic *(app1.py)*

---

## Candidate Ranking

Candidates are automatically categorized as:

- Good Fit
- Worth Reviewing
- Low Fit

---

## Export Features

- Download results as CSV
- Export filtered reports to Excel
- In-memory Excel generation using `BytesIO`

---

# Application Versions

The repository contains two application versions.

| File | Description |
|---|---|
| `app.py` | Basic resume evaluator with TF-IDF similarity and direct skill matching |
| `app1.py` | Enhanced evaluator with skill aliases, preferred skills, internship-aware scoring, and project relevance scoring |

---

## app.py Features

- Standard TF-IDF similarity
- Basic keyword skill matching
- Fixed final score formula
- Experience-based scoring

---

## app1.py Features

- Improved TF-IDF with bigrams
- English stop-word removal
- Skill aliases and normalization
- Required vs preferred skill scoring
- Internship-aware evaluation
- Project relevance scoring

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core Programming Language |
| Streamlit | Web Application Framework |
| PyPDF2 | PDF Text Extraction |
| pandas | Data Processing |
| scikit-learn | TF-IDF & Similarity Computation |
| openpyxl | Excel Export |
| Regular Expressions (`re`) | Pattern Matching |
| BytesIO | In-memory File Export |

---

# Project Structure

```text
Intern-Resume-Evaluator/
│
├── app.py
├── app1.py
├── intern_resume_evaluator_report.pdf
└── README.md
```

---

# Application Workflow

```text
JOB DESCRIPTION INPUT
          ↓
UPLOAD PDF RESUMES
          ↓
TEXT EXTRACTION
          ↓
SKILL & PROFILE ANALYSIS
          ↓
TF-IDF SIMILARITY COMPUTATION
          ↓
CANDIDATE SCORING
          ↓
RANKING & LABELING
          ↓
CSV / EXCEL EXPORT
```

---

# How It Works

## Step 1 — Enter Job Description

The recruiter enters a job or internship description into the Streamlit text area.

---

## Step 2 — Upload Resume PDFs

Users upload one or more candidate resumes in PDF format.

---

## Step 3 — Resume Text Extraction

The application extracts text from uploaded resumes using `PyPDF2`.

---

## Step 4 — Information Detection

The system identifies:

- Skills
- Degree keywords
- Experience indicators
- Email addresses
- Phone numbers

---

## Step 5 — Similarity Computation

The application computes resume relevance using:

- TF-IDF vectorization
- Cosine similarity
- Skill overlap
- Experience scoring

---

## Step 6 — Candidate Ranking

Candidates are ranked based on final fit scores and displayed in the Streamlit dashboard.

---

# Sample Resume Files

The following sample resume PDFs can be used for testing the application.

| Resume File |
|---|
| `AJAY-resume.pdf` |
| `ayesha_khan.pdf` |
| `Prajith-resume-new.pdf` |
| `priya_nair.pdf` |
| `resume_arjun_mehta.pdf` |
| `resume_kavita_reddy.pdf` |
| `rahul_verma.pdf` |
| `resume_neha_sharma.pdf` |
| `resume_sameer_khan.pdf` |
| `resume_rohan_iyer.pdf` |
| `Nivasini-resume-Feb-2026.pdf` |

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/Intern-Resume-Evaluator.git
cd Intern-Resume-Evaluator
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install streamlit pandas PyPDF2 scikit-learn openpyxl
```

---

# How to Run the Project

## Run Basic Version

```bash
streamlit run app.py
```

---

## Run Enhanced Version

```bash
streamlit run app1.py
```

---

After launching the app, open the local URL shown in the terminal.

Example:

```text
http://localhost:8501
```

---

# Output

The application displays a ranked results dashboard containing:

- Candidate scores
- Match labels
- Contact details
- Degree information
- Matched skills
- Missing skills
- Evaluation notes

---

## Export Options

Users can download:

- CSV reports
- Excel reports

for filtered candidate results.

---

# Scoring Logic

The final ranking score combines multiple components.

| Score Component | Purpose |
|---|---|
| TF-IDF Similarity | Measures resume relevance to JD |
| Skill Match Score | Measures matching technical skills |
| Experience Score | Estimates experience alignment |
| Project Score *(app1.py)* | Evaluates relevant project keywords |
| Internship Logic *(app1.py)* | Adjusts scoring for internships |

---

# Core Functionalities

## Resume Parsing

The application extracts readable content from uploaded PDF resumes.

---

## Skill Matching

Skills are identified through keyword matching and alias mapping.

---

## Candidate Ranking

Applicants are ranked using combined weighted scores.

---

## Report Generation

Results can be exported as:

- CSV
- Excel

for recruiter review.

---

# Challenges Solved

| Challenge | Solution |
|---|---|
| PDF text extraction inconsistencies | Implemented preprocessing and cleanup |
| Skill normalization | Added skill alias support in `app1.py` |
| Resume ranking accuracy | Combined multiple scoring components |
| Export handling | Used `BytesIO` for Excel generation |
| Internship evaluation | Added internship-aware scoring logic |

---

# Limitations

- The system relies mainly on keyword and pattern matching.
- Semantic understanding is limited.
- PDF extraction quality depends on resume formatting.
- Experience estimation is approximate.
- No advanced NLP or transformer embeddings are currently used.

---

# Future Improvements

Potential future enhancements include:

- Transformer-based semantic embeddings
- Advanced Named Entity Recognition (NER)
- DOCX resume support
- Recruiter-side filtering dashboards
- Candidate history tracking
- Resume visualization analytics
- AI-powered recommendation system
- Cloud deployment support

---

# Academic Purpose

This project was developed as a:

- Resume Screening Automation Project
- Streamlit Web Application Project
- NLP & Text Mining Practice Project
- AI-assisted Recruitment Workflow Simulation
- Internship Recruitment Automation System

---

# Repository Goals

This repository is intended for:

- Resume Projects
- GitHub Portfolio
- Streamlit Learning
- NLP Demonstration
- Recruitment Workflow Simulation
- Data Science Portfolio
- Internship Project Showcase

---


# Author

Developed by **Nivasini Muthukumaran**.

## Focus Areas

- Resume Screening Automation
- NLP & Text Processing
- Streamlit Development
- Candidate Ranking Systems
- AI-assisted Recruitment
- Data Analytics
