import streamlit as st
from prompts import get_technical_prompt_with_context
from utils import initialize_model, save_candidate_info, fetch_next_question

# Initialize Model Once
if "model_pipeline" not in st.session_state:
    st.session_state["model_pipeline"] = initialize_model()
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "answers" not in st.session_state:
    st.session_state["answers"] = {}

# Title and Introduction
st.title("TalentScout's Hiring Assistant")
st.write("Welcome to TalentScout's AI Assistant!")
st.write(
    "I’m here to help with the initial screening process by collecting your details "
    "and asking a few technical questions based on your expertise. Let's get started!"
)

# Candidate Information Form
if "candidate_info" not in st.session_state:
    st.subheader("Candidate Information")
    with st.form("candidate_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        position = st.text_input("Desired Position")
        location = st.text_input("Current Location")
        tech_stack = st.text_area(
            "Tech Stack",
            "List the programming languages, frameworks, databases, and tools you are proficient in (comma-separated).",
        )
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not first_name or not last_name or not email or not phone or not position or not location:
            st.warning("Please fill in all required fields.")
        else:
            st.session_state["candidate_info"] = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "experience": experience,
                "position": position,
                "location": location,
                "tech_stack": [tech.strip() for tech in tech_stack.split(",") if tech.strip()],
            }
            save_candidate_info(st.session_state["candidate_info"])
            st.success("Candidate information saved! Please proceed to the questions.")

# Technical Questions Section
if "candidate_info" in st.session_state:
    st.subheader("Technical Questions")
    candidate_info = st.session_state["candidate_info"]
    current_index = st.session_state["current_index"]
    tech_stack = candidate_info["tech_stack"]

    if current_index < len(tech_stack):
        # Fetch the next question
        next_question = fetch_next_question(
            candidate_info["experience"],
            candidate_info["position"],
            tech_stack,
            current_index,
            st.session_state["model_pipeline"],
        )

        if next_question:
            st.write(f"**Question for {tech_stack[current_index]}:** {next_question}")
            user_answer = st.text_input(
                f"Your Answer for {tech_stack[current_index]}",
                key=f"answer_{current_index}"
            )

            # Save the answer and move to the next question
            if st.button("Submit Answer", key=f"submit_{current_index}"):
                if not user_answer.strip():
                    st.warning("Answer cannot be empty. Please provide a valid response.")
                else:
                    st.session_state["answers"][tech_stack[current_index]] = user_answer.strip()
                    st.session_state["current_index"] += 1
        else:
            st.error("Could not generate a question. Skipping...")
            st.session_state["current_index"] += 1
    else:
        st.success("All questions have been answered. Thank you!")
        st.write("Your responses:")
        for tech, answer in st.session_state["answers"].items():
            st.write(f"**{tech}:** {answer}")

        if st.button("Start Over"):
            st.session_state.clear()
            st.experimental_rerun()
