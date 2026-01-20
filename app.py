import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# App title
st.title("🧠 Skill Gap Analyzer")

# Read CSV
df = pd.read_csv("data/job_roles.csv")

# Select job role
selected_role = st.selectbox(
    "Select a Job Role",
    df["role"].tolist()
)

# Get required skills
role_data = df[df["role"] == selected_role]
skills_string = role_data.iloc[0]["skills"]
required_skills = [skill.strip().lower() for skill in skills_string.split(",")]

# User skill input
user_input = st.text_input(
    "Enter your skills (comma separated)",
    placeholder="e.g. Python, Excel"
)

# Analyze button
if st.button("Analyze Skills"):
    if user_input.strip() == "":
        st.warning("Please enter your skills")
    else:
        user_skills = [skill.strip().lower() for skill in user_input.split(",")]

        matched_skills = set(required_skills).intersection(user_skills)
        missing_skills = set(required_skills) - matched_skills

        total_required = len(required_skills)
        matched_count = len(matched_skills)
        match_percentage = (matched_count / total_required) * 100

        # Display results
        st.subheader("📊 Skill Match Result")
        st.write(f"**Match Percentage:** {round(match_percentage, 2)} %")
        
        # 📊 Skills Overview Chart
        st.subheader("📊 Skills Overview")

        labels = ["Matched Skills", "Missing Skills"]
        values = [len(matched_skills), len(missing_skills)]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Count")
        ax.set_title("Matched vs Missing Skills")

        st.pyplot(fig)

        # 📈 Progress Bar
        st.subheader("📈 Overall Progress")
        st.progress(min(int(match_percentage), 100))


        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write("-", skill.title())
        else:
            st.write("No matched skills")

        st.subheader("❌ Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write("-", skill.title())
        else:
            st.write("No missing skills 🎉")

        # Learning roadmap
        st.subheader("📚 Learning Roadmap")
        week = 1
        for skill in missing_skills:
            st.write(f"Week {week}: Learn {skill.title()}")
            week += 1
