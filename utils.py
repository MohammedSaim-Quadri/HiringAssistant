import json
import os
import psycopg2
from dotenv import load_dotenv
import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from prompts import get_technical_prompt_with_context
from cryptography.fernet import Fernet

load_dotenv()

# Initialize Language Model
@st.cache_resource
def initialize_model():
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return pipeline("text2text-generation", 
                    model=model, 
                    tokenizer=tokenizer,
                    max_new_tokens=50,  # Limits length of generated text
                    temperature=0.5,    # Reduces randomness
                    device=-1 )


# Generate Questions
def generate_questions(experience, position, tech_stack, model_pipeline):
    questions = {}
    for tech in tech_stack:
        prompt = get_technical_prompt_with_context(experience, position, tech)
        try:
            response = model_pipeline(prompt)
            if response and isinstance(response, list) and "generated_text" in response[0]:
                clean_question = response[0]["generated_text"].strip()
                if clean_question.lower().startswith("generate"):
                    raise ValueError("Model returned the prompt instead of a question.")
                questions[tech] = clean_question
            else:
                raise ValueError("Unexpected response format.")
        except Exception as e:
            questions[tech] = f"Error generating question for {tech}: {e}"
    return questions


# Fetch Next Question
def fetch_next_question(experience, position,tech_stack, index, model_pipeline):
    if index >= len(tech_stack):
        return None
    
    tech = tech_stack[index]
    # Set difficulty based on experience
    if experience < 3:
        difficulty = "easy"
    elif 3 <= experience <= 7:
        difficulty = "medium"
    else:
        difficulty = "hard"
    prompt = get_technical_prompt_with_context(experience, position,tech, difficulty)
    
    try:
        print(f"DEBUG: Prompt sent to model: {prompt}")
        response = model_pipeline(prompt)
        if response and isinstance(response, list) and "generated_text" in response[0]:
            clean_question = response[0]["generated_text"].strip()
            print(f"DEBUG: Model response: {clean_question}")
            return clean_question
        else:
            raise ValueError("Unexpected reponse format.")
    except Exception as e:
        print(f"DEBUG: Error generating question: {e}")
        return f"Error generating question for {tech}:{e}"
    

#Generate save encryption key ( run this once and store the key securely)
def generate_key():
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as key_file:
        key_file.write(key)


#Load encryption key
def load_key():
    if not os.path.exists("encryption.key"):
        generate_key()
    with open("encryption.key", "rb") as key_file:
        return key_file.read()
    

# Encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    return encrypted_data


#decrypt data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)


# # save candidate info securely
# def save_candidate_info(info):
#     key = load_key()
#     encrypted_data = encrypt_data(info, key)

#     #save the encrypted data to json file
#     with open("candidata_data.json", "ab") as file:
#         file.write(encrypted_data + b"\n") # store each candidates data on a new line


# load all candidate info
def load_all_candidates():
    key= load_key()
    candidates = []
    try:
        with open("candidate_data.json", "rb") as file:
            for line in file:
                encrypted_data = line.strip()
                candidates.append(decrypt_data(encrypted_data,key))
    except FileNotFoundError:
        pass
    return candidates

# Initialize Database Connection
def init_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"), 
        port = os.getenv("DB_PORT"),         # From environment variables
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

# Save Candidate to Database
def save_to_db(candidate_info, answers):
    conn = init_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''INSERT INTO candidates 
            (first_name, last_name, email, phone, experience, position, location, tech_stack, answers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (
                candidate_info["first_name"],
                candidate_info["last_name"],
                candidate_info["email"],
                candidate_info["phone"],
                candidate_info["experience"],
                candidate_info["position"],
                candidate_info["location"],
                ','.join(candidate_info["tech_stack"]),
                json.dumps(answers),
            )
        )
        conn.commit()
    except Exception as e:
        raise Exception(f"Error saving to database: {e}")
    finally:
        cur.close()
        conn.close()

# Load All Candidates from Database
def load_all_candidates_from_db():
    conn = init_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM candidates")
        rows = cur.fetchall()
        candidates = [
            {
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "phone": row[4],
                "experience": row[5],
                "position": row[6],
                "location": row[7],
                "tech_stack": row[8].split(","),
                "answers": row[9],
            }
            for row in rows
        ]
        return candidates
    except Exception as e:
        raise Exception(f"Error loading from database: {e}")
    finally:
        cur.close()
        conn.close()