from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import pandas as pd
import random
import os
# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load teammates dataset from CSV
try:
    teammates_df = pd.read_csv("dataset1.csv")  
except Exception as e:
    st.error(f"Error loading CSV file: {e}")

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro") 

def get_gemini_response(question):
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

def allocate_tasks_to_teammates(tasks, teammates_df):
    # Allocate tasks to teammates based on their skills and details
    allocated_tasks = {}
    for task in tasks:
        # Match task requirements with teammates' skills
        # For demonstration purposes, let's assign tasks randomly
        allocated_teammate = random.choice(teammates_df['Name'].tolist())
        allocated_tasks[task] = allocated_teammate
    return allocated_tasks

# Initialize Streamlit app
st.set_page_config(page_title="Super Squad")
st.title("Super Squad")
st.sidebar.image("WhatsApp Image 2024-04-06 at 5.18.55 PM.jpeg", caption="Party planner pro", use_column_width=True)
st.header("Party planner Pro")

# Text input for user prompt
input_text = st.text_input("Input:", key="input")

# Button to trigger project planning
submit_button = st.button("Plan the project")

if submit_button and input_text:
    # Get Gemini response based on user prompt
    gemini_response = get_gemini_response(input_text)
    
    # Display Gemini response
    st.subheader("The Project Plan")
    tasks = []
    for chunk in gemini_response:
        task = chunk.text.strip()
        tasks.append(task)
        st.write(task)
    
    # Allocate tasks to teammates
    allocated_tasks = allocate_tasks_to_teammates(tasks, teammates_df)
    
    # Display allocated tasks with assigned teammates
    st.subheader("Allocated Tasks")
    for task, teammate in allocated_tasks.items():
        st.write(f"{task}: {teammate}")

# Display teammates dataset
st.subheader("Teammates Dataset")
if "teammates_df" in locals():
    st.dataframe(teammates_df)
else:
    st.error("Teammates dataset not loaded. Please check if the CSV file exists and is correctly formatted.")
