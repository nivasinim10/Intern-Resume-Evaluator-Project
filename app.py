import re
from io import BytesIO

import pandas as pd
import PyPDF2
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="Intern Resume Evaluator", layout="wide")


SKILL_BANK = [
    "python", "java", "c", "c++", "sql", "machine learning", "deep learning",
    "nlp", "data analysis", "data visualization", "pandas", "numpy",
    "scikit-learn", "tensorflow", "keras", "pytorch", "power bi", "tableau",
    "excel", "streamlit", "flask", "django", "html", "css", "javascript",
    "aws", "azure", "git", "matlab", "verilog"
]

DEGREE_KEYWORDS = [
    "b.tech", "m.tech", "b.e", "m.e", "bsc", "msc", "bca", "mca",
    "bachelor", "master", "phd", "diploma", "engineering"
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


def compute_text_match(job_text, resume_text):
    documents = [job_text, resume_text]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(matrix[0:1], matrix[1:2]).flatten()[0]
    return round(score * 100, 2)


def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "Not found"


def extract_phone(text):
    match = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text)
    return match.group(0) if match else "Not found"


def extract_skills(text):
    lowered_text = text.lower()
    skills_found = []

    for skill in SKILL_BANK:
        if skill in lowered_text:
            skills_found.append(skill)

    return sorted(set(skills_found))


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


def compare_required_skills(job_description, resume_text):
    required_skills = set()
    candidate_skills = set()

    lowered_job = job_description.lower()
    lowered_resume = resume_text.lower()

    for skill in SKILL_BANK:
        if skill in lowered_job:
            required_skills.add(skill)
        if skill in lowered_resume:
            candidate_skills.add(skill)

    matched = required_skills.intersection(candidate_skills)
    missing = required_skills - candidate_skills

    return matched, missing


def compute_skill_match(job_description, resume_text):
    matched_skills, missing_skills = compare_required_skills(job_description, resume_text)
    total_required = len(matched_skills) + len(missing_skills)

    if total_required == 0:
        return 0.0

    return round((len(matched_skills) / total_required) * 100, 2)


def compute_experience_match(job_description, candidate_years):
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


def compute_final_fit(text_score, skill_score, experience_score):
    final_score = (
        0.4 * text_score +
        0.4 * skill_score +
        0.2 * experience_score
    )
    return round(final_score, 2)


def get_review_label(score):
    if score >= 70:
        return "Good Fit"
    if score >= 45:
        return "Worth Reviewing"
    return "Low Fit"


def get_status_icon(label):
    if label == "Good Fit":
        return "🟢 Good Fit"
    if label == "Worth Reviewing":
        return "🟡 Worth Reviewing"
    return "🔴 Low Fit"


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

            final_fit_score = compute_final_fit(text_match, skill_match, experience_match)
            review_label = get_review_label(final_fit_score)

            matched_skills, missing_skills = compare_required_skills(job_description, original_text)
            all_skills = extract_skills(original_text)

            candidate_note = build_candidate_note(matched_skills, missing_skills, experience_years)

            all_results.append({
                "Resume Name": resume_file.name,
                "Role Fit Score": final_fit_score,
                "Text Match": text_match,
                "Skill Match": skill_match,
                "Experience Match": experience_match,
                "Review": review_label,
                "Status": get_status_icon(review_label),
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