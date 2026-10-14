import streamlit as st

from src.pdf_extractor import extract_text_from_pdf
from src.preprocessing import preprocess_text
from src.skill_extractor import extract_skill
from src.experience_extractor import extract_experience
from src.similarity import calculate_similarity
from src.semantic_similarity import calculate_semantic_similarity


# PAGE CONFIG


st.set_page_config(
    page_title="Resume-JD Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)



# SKILLS DATABASE


skills = [
    "python",
    "java",
    "c++",
    "javascript",
    "sql",
    "mongodb",
    "mysql",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "opencv",
    "flask",
    "django",
    "fastapi",
    "react",
    "node.js",
    "express",
    "git",
    "docker",
    "aws",
    "azure"
]



# HEADER


st.title("📄 Resume–Job Matching System")

st.write(
    "An NLP-powered application that analyzes your resume against a "
    "job description and identifies skill compatibility, experience "
    "requirements, and semantic similarity."
)

st.divider()



# FILE UPLOAD SECTION


st.subheader("📂 Upload Documents")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Resume")
    resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        key="resume"
    )

with col2:
    st.markdown("### 💼 Job Description")
    job_description = st.file_uploader(
        "Upload the job description",
        type=["pdf"],
        key="job_description"
    )


st.divider()



# ANALYSIS


if resume and job_description:

    st.success("Both documents uploaded successfully.")

    analyze = st.button(
        "🚀 Analyze Resume",
        use_container_width=True,
        type="primary"
    )

    if analyze:

        with st.spinner("Analyzing your resume..."):

            # Extract text
            resume_text = extract_text_from_pdf(resume)
            job_description_text = extract_text_from_pdf(job_description)

            # Preprocess
            resume_clean = preprocess_text(resume_text)
            job_description_clean = preprocess_text(job_description_text)

            # Semantic similarity
            similarity_score = calculate_similarity(
                resume_clean,
                job_description_clean
            )

            semantic_score = calculate_semantic_similarity(
            resume_clean,
            job_description_clean
            )


            # Extract skills
            resume_skills = extract_skill(
                resume_clean,
                skills
            )

            job_skills = extract_skill(
                job_description_clean,
                skills
            )

            # Convert to sets
            resume_set = set(resume_skills)
            job_set = set(job_skills)

            # Skill comparison
            matching_skills = resume_set.intersection(job_set)
            missing_skills = job_set.difference(resume_set)

            # Skill match percentage
            if len(job_set) > 0:
                match_percentage = (
                    len(matching_skills) / len(job_set)
                ) * 100
            else:
                match_percentage = 0

            # Experience
            resume_experience = extract_experience(
                resume_clean
            )

            job_experience = extract_experience(
                job_description_clean
            )

        st.success("Analysis completed successfully! 🎯")

        st.divider()


        
        # OVERALL SCORE
        

        st.subheader("📊 Match Overview")

        score_col1, score_col2, score_col3 = st.columns(3)

        with score_col1:
            st.metric(
                "🎯 Skill Match",
                f"{match_percentage:.1f}%"
            )

        with score_col2:
            st.metric(
                "🧠 Semantic Similarity",
                f"{similarity_score:.1f}%"
            )

        with score_col3:
            st.metric(
                "🛠️ Matching Skills",
                len(matching_skills)
            )


        st.divider()


        
        # SKILL ANALYSIS
        

        st.subheader("🛠️ Skill Analysis")

        skill_col1, skill_col2 = st.columns(2)

        with skill_col1:

            st.markdown("### ✅ Matching Skills")

            if matching_skills:

                for skill in sorted(matching_skills):
                    st.success(skill.title())

            else:
                st.info("No matching skills found.")


        with skill_col2:

            st.markdown("### ❌ Missing Skills")

            if missing_skills:

                for skill in sorted(missing_skills):
                    st.error(skill.title())

            else:
                st.success(
                    "Excellent! No required skills are missing."
                )


        st.divider()


        
        # EXPERIENCE ANALYSIS
        

        st.subheader("💼 Experience Analysis")

        exp_col1, exp_col2 = st.columns(2)

        with exp_col1:

            st.markdown("### 👤 Resume Experience")

            st.metric(
                "Experience",
                f"{resume_experience}"
            )


        with exp_col2:

            st.markdown("### 📋 Required Experience")

            st.metric(
                "Required",
                f"{job_experience}"
            )


        st.divider()


        # -------------------------------------------------
        # SEMANTIC SIMILARITY
        # -------------------------------------------------

        st.subheader("🧠 Semantic Similarity")

        st.write(
            "Semantic similarity measures how closely the content "
            "of your resume matches the job description."
        )

        st.progress(
            min(int(similarity_score), 100)
        )

        st.metric(
            "Resume–Job Description Similarity",
            f"{similarity_score:.1f}%"
        )


        st.divider()


        # -------------------------------------------------
        # FINAL VERDICT
        # -------------------------------------------------

        st.subheader("🏆 Final Assessment")

        overall_score = (
            match_percentage * 0.6
            + similarity_score * 0.4
        )

        if overall_score >= 80:

            st.success(
                f"🔥 Strong Match — Overall Compatibility: "
                f"{overall_score:.1f}%"
            )

            st.write(
                "Your resume aligns very well with the job "
                "description. You appear to be a strong candidate."
            )

        elif overall_score >= 60:

            st.warning(
                f"👍 Good Match — Overall Compatibility: "
                f"{overall_score:.1f}%"
            )

            st.write(
                "Your resume has good alignment with the role, "
                "but improving some missing skills could strengthen "
                "your application."
            )

        else:

            st.error(
                f"⚠️ Low Match — Overall Compatibility: "
                f"{overall_score:.1f}%"
            )

            st.write(
                "There is a significant gap between your resume "
                "and the job requirements. Consider developing "
                "the missing skills."
            )


        # -------------------------------------------------
        # DOCUMENT INFORMATION
        # -------------------------------------------------

        st.divider()

        with st.expander("📄 Document Information"):

            info_col1, info_col2 = st.columns(2)

            with info_col1:

                st.write("**Resume:**")
                st.write(resume.name)

            with info_col2:

                st.write("**Job Description:**")
                st.write(job_description.name)


        #SIMILARITY COMPARISON

        st.subheader("🧠 Text Similarity Comparison")

        st.write(
            "Compare traditional TF-IDF similarity with "
            "Word2Vec-based document similarity."
        )

        sim_col1, sim_col2 = st.columns(2)

        with sim_col1:

            st.markdown("### 📊 TF-IDF Similarity")

            st.metric(
                "Resume–JD Similarity",
                f"{similarity_score:.2f}%"
            )

            st.progress(
                min(max(float(similarity_score) / 100, 0.0), 1.0)
            )

            st.caption(
                "Measures similarity using weighted word frequencies."
            )

        with sim_col2:

            st.markdown("### 🧠 Word2Vec Similarity")

            st.metric(
                "Resume–JD Similarity",
                f"{semantic_score:.2f}%"
            )

            st.progress(
                min(max(float(semantic_score) / 100, 0.0), 1.0)
            )

            st.caption(
                "Compares averaged pretrained word embeddings."
            )

        

        st.divider()


        


else:

    st.info(
        "👆 Upload both your resume and the job description "
        "to start the analysis."
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Resume–Job Matching System • NLP Project • "
    "Built with Python & Streamlit"
)

