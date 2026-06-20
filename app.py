import streamlit as st
import pandas as pd

from src.score_jobs import score_job
from src.collect_adzuna import collect_adzuna_jobs


st.title("CyberRoleFit Pipeline")

st.write("This dashboard analyzes cybersecurity and networking job postings.")

st.sidebar.header("Job Search Settings")

search_term = st.sidebar.text_input("Search term", "SOC Analyst")
location = st.sidebar.text_input("Location", "Dallas, TX")
results_per_page = st.sidebar.slider("Results per page", 5, 25, 10)

if st.sidebar.button("Search Adzuna Jobs"):
    with st.spinner("Collecting jobs from Adzuna..."):
        jobs = collect_adzuna_jobs(
            search_term=search_term,
            location=location,
            results_per_page=results_per_page,
        )

    if not jobs:
        st.warning("No jobs were returned from Adzuna for this search.")
    else:
        scored_jobs = [score_job(job) for job in jobs]
        df = pd.DataFrame(scored_jobs)

        st.subheader("Scored Job Postings")

        st.dataframe(
            df[
                [
                    "title",
                    "company",
                    "location",
                    "fit_score",
                    "decision",
                    "source",
                    "created",
                ]
            ]
        )

        selected_job = st.selectbox("Select a job to view scoring reasons:", df["title"])

        job_details = df[df["title"] == selected_job].iloc[0]

        st.subheader(selected_job)

        st.write(f"**Company:** {job_details['company']}")
        st.write(f"**Location:** {job_details['location']}")
        st.write(f"**Decision:** {job_details['decision']}")
        st.write(f"**Fit Score:** {job_details['fit_score']}")
        st.write(f"**Source:** {job_details['source']}")
        st.write(f"**Created:** {job_details['created']}")

        if job_details.get("redirect_url"):
            st.link_button("Open Job Posting", job_details["redirect_url"])

        st.write("**Job Description:**")
        st.write(job_details["description"])

        st.write("**Scoring Reasons:**")
        for reason in job_details["reasons"]:
            st.write(f"- {reason}")
else:
    st.info("Use the sidebar to search Adzuna job postings.")