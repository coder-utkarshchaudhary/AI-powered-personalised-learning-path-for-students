import os
import json
import streamlit as st
from dotenv import load_dotenv
from utils import get_llm_response

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@st.cache_data
def load_dataset():
    try:
        with open("mock dataset generation/datasets/dataset.json", "r") as _file:
            return json.load(_file)
    except FileNotFoundError:
        st.error("Could not load the dataset. Please check the file location.")
        raise

def get_system_prompt(dataset):
    return f"""
    You are an experienced professor specializing in creating personalized study plans for students. 
    Use the dataset provided to answer queries comprehensively. If no information is available in the dataset, 
    search the internet, validate the links, and return relevant results.

    Dataset: {dataset}
    """

_format = """{
    "Workshops" : [<List of workshops>],
    "Activities" : [<List of activities>],
    "Tasks" : [<List of tasks>],
    "Mentors" : [<List of mentors to connect with their social media links>]
}
"""

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "student_attributes" not in st.session_state:
        st.session_state.student_attributes = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"

def format_user_prompt(attributes):
    sections = {
        "strengths": "Strengths",
        "weaknesses": "Weaknesses",
        "interests": "Interests",
        "learning_style": "Learning Style",
        "learning_challenges": "Learning Challenges",
        "goals": "Goals",
        "availability": "Availability"
    }
    
    formatted_sections = ["Student Profile:"]
    for key, title in sections.items():
        if attributes.get(key):
            value = attributes[key]
            if isinstance(value, list):
                value = ", ".join(v.strip() for v in value if v.strip())
            elif isinstance(value, str):
                value = value.strip()
            if value:
                formatted_sections.append(f"   * {title}: {value}")
    
    return "\n".join(formatted_sections)

def generate_initial_study_plan(attributes):
    user_query = f"""
    A student has the following characteristics: {attributes}. 
    Create a detailed study plan including workshops, tasks, activities, and mentors. 
    Format: {_format}
    """
    
    with st.spinner("Generating your personalized study plan..."):
        dataset = load_dataset()
        system_prompt = get_system_prompt(dataset)
        response = get_llm_response(
            system_query=system_prompt,
            user_query=user_query,
            openai_api_key=OPENAI_API_KEY,
            external_user_id="user"
        )
        return response
    
def format_mentor(mentor):
    return f"* **{mentor['Name']}** - {mentor['Expertise']}\n  [Connect on LinkedIn]({mentor['Social Media']})"


def display_chat_message(message, is_user=False):
    with st.chat_message("user" if is_user else "assistant"):
        if is_user:
            st.markdown(message)
        else:
            try:
                study_plan = json.loads(message)
                
                if "Workshops" in study_plan:
                    st.markdown("### Workshops")
                    for workshop in study_plan["Workshops"]:
                        st.markdown(f"* {workshop}")
                    st.markdown("")

                if "Activities" in study_plan:
                    st.markdown("### Activities")
                    for activity in study_plan["Activities"]:
                        st.markdown(f"* {activity}")
                    st.markdown("")

                if "Tasks" in study_plan:
                    st.markdown("### Tasks")
                    for task in study_plan["Tasks"]:
                        st.markdown(f"* {task}")
                    st.markdown("")

                if "Mentors" in study_plan:
                    st.markdown("### Mentors")
                    for mentor in study_plan["Mentors"]:
                        st.markdown(f"* **{mentor['Name']}** - {mentor['Expertise']}\n  [Connect on LinkedIn]({mentor['Social Media']})")
                    st.markdown("")

            except json.JSONDecodeError:
                st.error("Failed to parse the response. Please try again.")

def student_attributes_form():
    st.markdown("### Enter Student Information")
    
    with st.form("student_attributes_form"):
        fields = {
            "strengths": "Strengths (e.g., problem-solving, creativity)",
            "weaknesses": "Weaknesses (e.g., math, grammar)",
            "interests": "Interests (e.g., astronomy, programming)",
            "learning_style": "Learning Style (e.g., visual, auditory)",
            "learning_challenges": "Learning Challenges (e.g., short attention span)",
            "goals": "Goals (e.g., become a software engineer)",
            "availability": "Availability (e.g., 2 hours daily, weekends)"
        }
        
        form_data = {field: st.text_input(label) for field, label in fields.items()}
        submitted = st.form_submit_button("Generate Study Plan")
        
        if submitted:
            st.session_state.student_attributes = {
                key: value.split(",") if value and key != "learning_style" else value
                for key, value in form_data.items()
            }
            st.session_state.current_page = "chat"
            
            user_prompt = format_user_prompt(st.session_state.student_attributes)
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            
            initial_response = generate_initial_study_plan(st.session_state.student_attributes)
            st.session_state.messages.append({"role": "assistant", "content": initial_response})
            
            st.rerun()

def chat_interface():
    st.markdown("### Your Personalized Learning Assistant")
    
    for message in st.session_state.messages:
        display_chat_message(message["content"], message["role"] == "user")
    
    if st.button("Start New Plan"):
        st.session_state.messages = []
        st.session_state.student_attributes = None
        st.session_state.current_page = "form"
        st.rerun()

def main():
    initialize_session_state()
    
    if st.session_state.current_page == "landing":
        _, col2, __ = st.columns([1, 6, 1])
        with col2:
            st.title("AI Study Plan Assistant")
            st.markdown("### Welcome! Let's create your personalized study plan.")
            if st.button("Start"):
                st.session_state.current_page = "form"
                st.rerun()
    
    elif st.session_state.current_page == "form":
        student_attributes_form()
    
    elif st.session_state.current_page == "chat":
        chat_interface()

if __name__ == "__main__":
    main()