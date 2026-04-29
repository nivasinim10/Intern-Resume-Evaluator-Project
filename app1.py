import re
from io import BytesIO

import pandas as pd
import PyPDF2
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Intern Resume Evaluator", layout="wide")

SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "c": ["c"],
    "c++": ["c++", "cpp"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "machine learning": ["machine learning", "ml", "predictive modeling"],
    "deep learning": ["deep learning", "dl", "neural networks", "ann", "cnn", "lstm"],
    "nlp": ["nlp", "natural language processing", "text mining"],
    "data analysis": ["data analysis", "analytics"],
    "data visualization": ["data visualization", "visualization", "viz"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow", "tf"],
    "keras": ["keras"],
    "pytorch": ["pytorch", "torch"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "excel": ["excel"],
    "streamlit": ["streamlit"],
    "flask": ["flask"],
    "django": ["django"],
    "html": ["html"],
    "css": ["css"],
    "javascript": ["javascript", "js"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "git": ["git", "github"],
    "matlab": ["matlab"],
    "verilog": ["verilog"]
}

DEGREE_KEYWORDS = [
    "b.tech", "m.tech", "b.e", "m.e", "bsc", "msc", "bca", "mca",
    "bachelor", "master", "phd", "diploma", "engineering"
]

PROJECT_KEYWORDS = [
    "project", "built", "developed", "implemented", "deployed",
    "classification", "prediction", "analysis", "dashboard",
    "nlp", "machine learning", "deep learning", "web app"
]

def extract_resume_text(pdf_file):
    collected_text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            collected_text += page_text + " "
    return collected_text.strip()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s\+\.]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def is_internship_role(job_description):
    lowered = job_description.lower()
    return any(word in lowered for word in ["intern", "internship", "fresher", "trainee", "entry level"])

def extract_skills(text):
    lowered_text = text.lower()
    skills_found = set()

    for canonical_skill, aliases in SKILL_ALIASES.items():
        if any(alias in lowered_text for alias in aliases):
            skills_found.add(canonical_skill)

    return sorted(skills_found)

def extract_job_skills(job_description):
    lowered_job = job_description.lower()
    required = set()
    preferred = set()

    required_markers = ["must have", "required", "should have", "looking for", "need"]
    preferred_markers = ["preferred", "nice to have", "good to have", "plus"]

    for canonical_skill, aliases in SKILL_ALIASES.items():
        if any(alias in lowered_job for alias in aliases):
            if any(marker in lowered_job for marker in preferred_markers):
                preferred.add(canonical_skill)
            else:
                required.add(canonical_skill)

    if not required and not preferred:
        return set(), set()

    return required, preferred

def compute_skill_match(job_description, resume_text):
    required_skills, preferred_skills = extract_job_skills(job_description)
    candidate_skills = set(extract_skills(resume_text))

    if not required_skills and not preferred_skills:
        return 0.0

    required_matched = required_skills.intersection(candidate_skills)
    preferred_matched = preferred_skills.intersection(candidate_skills)

    required_score = (len(required_matched) / len(required_skills)) if required_skills else 0
    preferred_score = (len(preferred_matched) / len(preferred_skills)) if preferred_skills else 0

    return round((required_score * 0.75 + preferred_score * 0.25) * 100, 2)

def compute_text_match(job_text, resume_text):
    documents = [job_text, resume_text]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(matrix[0:1], matrix[1:2]).flatten()[0]
    return round(score * 100, 2)

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    match = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text)
    return match.group(0) if match else "Not found"

def extract_degree_info(text):
    lowered_text = text.lower()
    found_degrees = []

    for keyword in DEGREE_KEYWORDS:
        if keyword in lowered_text:
            found_degrees.append(keyword)

    if found_degrees:
        return ", ".join(sorted(set(found_degrees)))
    return "Not clearly mentioned"

def extract_experience_years(text):
    lowered_text = text.lower()
    patterns = [
        r"(\d+)\+?\s+years",
        r"(\d+)\+?\s+yrs",
        r"experience\s+of\s+(\d+)\s+years",
        r"(\d+)\s+year[s]?\s+of\s+experience"
    ]

    years_list = []
    for pattern in patterns:
        matches = re.findall(pattern, lowered_text)
        for value in matches:
            try:
                years_list.append(int(value))
            except ValueError:
                continue

    return max(years_list) if years_list else 0

def compute_experience_match(job_description, candidate_years):
    if is_internship_role(job_description):
        return 100.0

    lowered_job = job_description.lower()
    required_years = 0

    patterns = [
        r"(\d+)\+?\s+years",
        r"(\d+)\+?\s+yrs",
        r"minimum\s+(\d+)\s+years",
        r"at least\s+(\d+)\s+years"
    ]

    for pattern in patterns:
        found = re.search(pattern, lowered_job)
        if found:
            required_years = int(found.group(1))
            break

    if required_years == 0:
        return 50.0

    if candidate_years >= required_years:
        return 100.0

    return round((candidate_years / required_years) * 100, 2)

def compute_project_score(resume_text, job_description):
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    project_hits = sum(1 for kw in PROJECT_KEYWORDS if kw in resume_lower and kw in job_lower)
    return round(min(project_hits / 5 * 100, 100), 2)

def build_candidate_note(matched_skills, missing_skills, experience_years):
    if matched_skills and not missing_skills:
        return f"Strong skill alignment with around {experience_years} year(s) of visible experience."

    if matched_skills and missing_skills:
        return (
            f"Shows relevant skills like {', '.join(sorted(list(matched_skills))[:3])}, "
            f"but still misses {', '.join(sorted(list(missing_skills))[:3])}."
        )

    return "Basic profile details were found, but the role alignment looks limited."

def create_excel_download(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Resume Review")
    return output.getvalue()

st.title("Intern Resume Evaluator")
st.write(
    "Upload resumes and compare them against a role description. "
    "The tool gives a quick fit score, skill comparison, and a simple review summary."
)

job_description = st.text_area(
    "Paste the job or internship description",
    height=220,
    placeholder="Example: We are looking for a Data Science Intern with Python, SQL, pandas, machine learning basics, data preprocessing, and problem-solving skills..."
)

uploaded_resumes = st.file_uploader(
    "Upload resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Evaluate resumes"):
    if not job_description.strip():
        st.warning("Please paste the job description first.")
    elif not uploaded_resumes:
        st.warning("Please upload at least one resume PDF.")
    else:
        cleaned_job_text = preprocess_text(job_description)
        all_results = []

        for resume_file in uploaded_resumes:
            original_text = extract_resume_text(resume_file)
            cleaned_resume_text = preprocess_text(original_text)

            text_match = compute_text_match(cleaned_job_text, cleaned_resume_text)
            skill_match = compute_skill_match(job_description, original_text)
            experience_years = extract_experience_years(original_text)
            experience_match = compute_experience_match(job_description, experience_years)
            project_score = compute_project_score(original_text, job_description)

            if is_internship_role(job_description):
                final_fit_score = round(
                    0.45 * skill_match +
                    0.25 * text_match +
                    0.15 * experience_match +
                    0.15 * project_score,
                    2
                )
            else:
                final_fit_score = round(
                    0.35 * text_match +
                    0.45 * skill_match +
                    0.20 * experience_match,
                    2
                )

            if final_fit_score >= 70:
                review_label = "Good Fit"
            elif final_fit_score >= 45:
                review_label = "Worth Reviewing"
            else:
                review_label = "Low Fit"

            if review_label == "Good Fit":
                status_icon = "🟢 Good Fit"
            elif review_label == "Worth Reviewing":
                status_icon = "🟡 Worth Reviewing"
            else:
                status_icon = "🔴 Low Fit"

            candidate_skills = set(extract_skills(original_text))
            required_skills, _ = extract_job_skills(job_description)
            matched_skills = required_skills.intersection(candidate_skills)
            missing_skills = required_skills - candidate_skills

            all_skills = extract_skills(original_text)
            candidate_note = build_candidate_note(matched_skills, missing_skills, experience_years)

            all_results.append({
                "Resume Name": resume_file.name,
                "Role Fit Score": final_fit_score,
                "Text Match": text_match,
                "Skill Match": skill_match,
                "Experience Match": experience_match,
                "Project Score": project_score,
                "Review": review_label,
                "Status": status_icon,
                "Email": extract_email(original_text),
                "Phone": extract_phone(original_text),
                "Degree Info": extract_degree_info(original_text),
                "Experience Seen (Years)": experience_years,
                "Skill Snapshot": ", ".join(all_skills) if all_skills else "Not found",
                "Matched Skills": ", ".join(sorted(matched_skills)) if matched_skills else "None",
                "Missing Skills": ", ".join(sorted(missing_skills)) if missing_skills else "None",
                "Quick Note": candidate_note
            })

        results_df = pd.DataFrame(all_results)
        results_df = results_df.sort_values(by="Role Fit Score", ascending=False).reset_index(drop=True)

        top_candidate = results_df.iloc[0]
        good_fit_count = (results_df["Review"] == "Good Fit").sum()
        review_count = (results_df["Review"] == "Worth Reviewing").sum()
        low_fit_count = (results_df["Review"] == "Low Fit").sum()

        st.success("Resume evaluation finished.")

        metric1, metric2, metric3, metric4 = st.columns(4)
        metric1.metric("Total Resumes", len(results_df))
        metric2.metric("Good Fit", int(good_fit_count))
        metric3.metric("Worth Reviewing", int(review_count))
        metric4.metric("Top Fit Score", f"{top_candidate['Role Fit Score']}")

        st.subheader("Best matching profile")
        st.info(
            f"{top_candidate['Resume Name']} has the highest role fit score of "
            f"{top_candidate['Role Fit Score']} and is marked as {top_candidate['Status']}."
        )
        st.write(f"**Quick Note:** {top_candidate['Quick Note']}")
        st.write(f"**Matched Skills:** {top_candidate['Matched Skills']}")
        st.write(f"**Missing Skills:** {top_candidate['Missing Skills']}")

        st.subheader("View by review type")
        selected_reviews = st.multiselect(
            "Choose which profiles you want to see",
            options=["Good Fit", "Worth Reviewing", "Low Fit"],
            default=["Good Fit", "Worth Reviewing", "Low Fit"]
        )

        filtered_results = results_df[results_df["Review"].isin(selected_reviews)].copy()
        final_display = filtered_results.drop(columns=["Review"])

        st.subheader("Resume analysis table")
        st.dataframe(final_display, use_container_width=True)

        csv_file = filtered_results.to_csv(index=False).encode("utf-8")
        excel_file = create_excel_download(filtered_results)

        download_col1, download_col2 = st.columns(2)

        with download_col1:
            st.download_button(
                label="Download CSV Report",
                data=csv_file,
                file_name="intern_resume_evaluation.csv",
                mime="text/csv"
            )

        with download_col2:
            st.download_button(
                label="Download Excel Report",
                data=excel_file,
                file_name="intern_resume_evaluation.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )