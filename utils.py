import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from prompts import get_technical_prompt_with_context
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
                    top_p=0.9,          # Allows controlled diversity
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


# Save Candidate Info
def save_candidate_info(info):
    # Here we can save info to a database or a file
    pass

# Fetch Next Question
def fetch_next_question(experience, position,tech_stack, index, model_pipeline):
    if index >= len(tech_stack):
        return None
    tech = tech_stack[index]
    prompt = get_technical_prompt_with_context(experience, position,tech)
    print(f"DEBUG: Prompt sent to model: {prompt}")
    response = model_pipeline(prompt)
    print(f"DEBUG: Model response: {response[0]['generated_text']}")
    return response[0]["generated_text"].strip()