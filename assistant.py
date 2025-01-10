import json
import streamlit as st
from prompts import get_technical_prompt_with_context
from utils import initialize_model, fetch_next_question, load_all_candidates_from_db,save_to_db

# Initialize Model Once
if "model_pipeline" not in st.session_state:
    st.session_state["model_pipeline"] = initialize_model()
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "answers" not in st.session_state:
    st.session_state["answers"] = {}

# Sidebar for Admin Login
def admin_login():
    st.sidebar.title("Admin Login")
    st.sidebar.write("Please authenticate to access the admin dashboard.")

    # Simple Password Authentication
    admin_username = st.sidebar.text_input("Admin Username")
    admin_password = st.sidebar.text_input("Admin Password", type="password")
    
    if st.sidebar.button("Login"):
        if authenticate_admin(admin_username, admin_password):
            st.session_state["admin_logged_in"] = True
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid credentials. Access denied.")

# Admin Authentication Function
def authenticate_admin(username, password):
    # Replace with your desired username and password
    valid_username = "admin"
    valid_password = "admin123"

    return username == valid_username and password == valid_password

# Page Navigation
if "admin_logged_in" in st.session_state and st.session_state["admin_logged_in"]:
    # Redirect to Admin Dashboard
    st.title("Admin Dashboard")
    st.subheader("Candidate Information")

    # Fetch all candidates from the database
    candidates = load_all_candidates_from_db()
    if candidates:
        for idx, candidate in enumerate(candidates, 1):
            st.write(f"### Candidate {idx}")
            st.json(candidate)
    else:
        st.warning("No candidate data found.")

    # Logout Option
    if st.button("Logout"):
        del st.session_state["admin_logged_in"]
        st.experimental_rerun()
else:
    # Admin Login and Default Candidate Info Collection
    admin_login()

    st.title("AI Hiring Assistant")
    # Your existing candidate form and questions logic here
    st.write("Welcome to AI Hiring Assistant!")
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
                # save_candidate_info(st.session_state["candidate_info"])
                st.success("Candidate information saved! Please proceed to the questions.")

    # Technical Questions Section
    if "candidate_info" in st.session_state:
        st.subheader("Technical Questions")
        candidate_info = st.session_state["candidate_info"]
        current_index = st.session_state["current_index"]
        tech_stack = candidate_info["tech_stack"]

        if current_index < len(tech_stack):
            # Check if question is already generated for the current index
            if f"question_{current_index}" not in st.session_state:
                # Fetch the next question
                next_question = fetch_next_question(
                    candidate_info["experience"],
                    candidate_info["position"],
                    tech_stack,
                    current_index,
                    st.session_state["model_pipeline"],
                )
                st.session_state[f"question_{current_index}"] = next_question
            else:
                next_question = st.session_state[f"question_{current_index}"]

            
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
                    st.session_state["answers"][tech_stack[current_index]] = {
                        "question": next_question,
                        "answer": user_answer.strip(),
                    }
                    st.session_state["current_index"] += 1
        else:
            st.success("All questions have been answered. Thank you!")
            st.write("Your responses:")
            for tech, data in st.session_state["answers"].items():
                st.write(f"**{tech}:**")
                # Debugging: Log the type and raw value of `data`
                st.write(f"Debugging data: (Type: {type(data)}) Raw Value: {data}")
                if isinstance(data, str):
                    try:
                        data = json.loads(data)  # Attempt to parse string as JSON
                    except json.JSONDecodeError:
                        st.error(f"Invalid data format for {tech}. Data: {data}")
                        continue
                if isinstance(data, dict) and "question" in data and "answer" in data:
                    st.write(f"- **Question:** {data['question']}")
                    st.write(f"- **Answer:** {data['answer']}")
                else:
                    st.warning(f"Unexpected format for {tech}: {data}")

            # save candidate data securely
            candidate_data = {
                "personal_details" : st.session_state["candidate_info"],
                "answers": st.session_state["answers"],
            }
            save_to_db(candidate_data["personal_details"], candidate_data["answers"])
            st.success("Your responses have been saved!")

            if st.button("Start Over"):
                st.session_state.clear()
                st.experimental_rerun()
