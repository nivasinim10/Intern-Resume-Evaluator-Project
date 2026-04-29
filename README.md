Intern Resume Evaluator
A Streamlit-based resume screening application that compares uploaded PDF resumes against a job or internship description and ranks candidates using text similarity, skill matching, and experience-based scoring.
Overview
This project is designed to reduce manual resume screening effort by extracting resume text, identifying useful profile details, and generating ranked candidate results in a browser-based interface. The workflow supports PDF upload, job-description matching, score-based ranking, result filtering, and report export in CSV and Excel formats.
Two application versions are included in the project:
•	app.py: a simpler version with direct skill matching, standard TF-IDF similarity, and a fixed final score formula using text, skill, and experience scores.
•	app1.py: an enhanced version with skill aliases, required-versus-preferred skill handling, internship-aware scoring, project relevance scoring, and improved TF-IDF settings with bigrams and English stop-word removal.
Features
•	Upload one or more resume PDFs through a Streamlit interface.
•	Paste a job or internship description for comparison.
•	Extract candidate email, phone number, degree keywords, skills, and visible experience indicators from resume text.
•	Compute text match using TF-IDF and cosine similarity.
•	Rank candidates with a final fit score and assign labels such as Good Fit, Worth Reviewing, and Low Fit.
•	Export filtered results as CSV and Excel files.
Tech Stack
•	Python
•	Streamlit
•	PyPDF2
•	pandas
•	scikit-learn
•	openpyxl
•	Regular expressions (re)
•	BytesIO for in-memory Excel export.
•	Project Structure
.
├── app.py
├── app1.py
├── intern_resume_evaluator_report.pdf
└── README.md

How It Works
1.	Enter a job or internship description in the text area.
2.	Upload one or more PDF resumes.
3.	The app extracts and preprocesses text from each resume using PyPDF2 and regular-expression-based cleanup.
4.	It detects skills, education cues, contact details, and experience indicators from resume content.
5.	It calculates text similarity, skill match, and experience match; app1.py also adds project scoring and internship-aware logic.
6.	It ranks candidates and displays the results in a Streamlit dashboard with download options.
Sample Resume Files
The attached resume PDFs below can be used to test the application by uploading them through the Streamlit interface as sample candidate resumes.
•	AJAY-resume.pdf 
•	ayesha_khan.pdf 
•	Prajith-resume-new.pdf 
•	priya_nair.pdf 
•	resume_arjun_mehta.pdf 
•	resume_kavita_reddy.pdf 
•	rahul_verma.pdf
•	resume_neha_sharma.pdf 
•	resume_sameer_khan.pdf 
•	resume_rohan_iyer.pdf 
•	Nivasini-resume-Feb-2026.pdf 
Installation
1.	Clone or download the project files.
2.	Create and activate a Python virtual environment.
3.	Install the required packages:
pip install streamlit pandas PyPDF2 scikit-learn openpyxl

Run the App
Run either version with Streamlit:
streamlit run app.py

or
streamlit run app1.py

Then open the local URL shown in the terminal, usually http://localhost:8501.
app.py vs app1.py
<img width="682" height="351" alt="image" src="https://github.com/user-attachments/assets/263e01e5-1e49-41b8-99d1-caad91a14fb1" />
Aspect	app.py	app1.py
Skill source	Uses a flat skill list for direct matching.	Uses aliases mapped to canonical skills.
Text similarity	Uses standard TF-IDF settings.	Uses TF-IDF with bigrams and English stop-word removal.
Skill logic	Matches skills mentioned in both job description and resume without priority separation.	Separates required and preferred skills and weights them differently.
Internship awareness	No special internship handling.	Detects internship roles and adapts scoring.
Project score	Not included.	Included for internship-oriented evaluation.
Complexity	Easier to explain and present.	More advanced and closer to practical shortlisting.



Output
The application displays a ranked results table with candidate scores, review labels, contact details, degree information, matched skills, missing skills, and a short evaluation note. It also provides downloadable CSV and Excel reports for filtered results.
Limitations
•	The system relies mainly on keyword and pattern matching, so it may miss semantically similar skills written in unexpected ways.
•	PDF extraction quality depends on the original resume format
•	Experience estimation is approximate and based on visible year patterns in the text.
•	The current implementation does not use semantic embeddings, advanced NER, or learned classification models.
Future Improvements
Potential extensions mentioned in the report include semantic skill matching with transformer embeddings, stronger resume parsing, DOCX support, visualization dashboards, recruiter-side filtering, and candidate history tracking.
Author
Nivasini Muthukumaran.
