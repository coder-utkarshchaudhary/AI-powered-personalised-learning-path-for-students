# **AI POWERED PERSONALISED LEARNING PATH FOR STUDENTS**

## **Overview**
This project aims to develop an AI-powered system for creating personalized learning paths for students. Leveraging user-defined attributes, this system generates tailored study plans that include workshops, tasks, activities, and mentorship recommendations.

---

## **Implementation Details**
1. **LLM Integration**:
    - The entire solution is powered by OpenAI's GPT-4o model.
    - The generated dataset is used to finetune "session parameters" for instances created during production use. This ensures accurate, reliable and contextually appropriate answers.
    - Explicitly passed System Prompts which help increase accuracy of the task without overhead of computation resources needed for finetuning model parameters.

2. **Mock Dataset Generation**:
    - Generated mock dataset with 7 student centric attributes.
        - Strengths
        - Weaknesses
        - Interests
        - Learning Style
        - Learning Challenges
        - Goals
        - Availability

    - All the attibutes represent a key area that shape the learning plan. Clever prompt engineering ensures learning paths generated suit the needs of the students.

3. **Unstructured Data Handling**:
    - JSON parsing and processing for creation of labelled (student_attribute, study_plan) labels for finetuning "session parameters".

4. **Web Interface**:
    - Developed using StreamLit to git a GUI for the student to interact with the model.
    - A single-session chatbot interface where users can input attributes and query the generated plan.

---

## **How to Run?**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/coder-utkarshchaudhary/AI-powered-personalised-learning-path-for-students.git
   cd AI-powered-personalised-learning-path-for-students
   ```

2. **Install Dependencies**:
   Ensure `pip` is installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the Application**:
   Start the Streamlit application:
   ```bash
   streamlit run main.py
   ```

---

## **Final Submission**
- **Codebase**: [Link to GitHub repository](https://github.com/coder-utkarshchaudhary/AI-powered-personalised-learning-path-for-students.git)
- **Video**: Click on image(s) below for the video demo<br><a href="https://drive.google.com/file/d/13izGcUk4rhv2NAgRUMfvRE8oTyFhvtSb/view?usp=sharing"><img src="images/Form Window.png" alt="Form Window"></a><br><a href="https://drive.google.com/file/d/13izGcUk4rhv2NAgRUMfvRE8oTyFhvtSb/view?usp=sharing"><img src="images/Chat Window.png" alt="Chat Window"></a>
---

## **Notes**
1. The project is powered by GPT-4o model. The model's API is access via On-Demand platform. The code will not directly work for OpenAI API calls directly. Please modify the ```get_llm_response``` function in ```utils.py```.

    #### Blockers and Possible Fixes:
    1.  LLMs can't access and obtain information about user profiles from social media websites. Hence a lot of entires for mentors in the dataset are "John Doe" or "Jane Doe" or "Emily ...". This can be easily fixed by developing a _vector database of mentor profiles_ and establishing a _RAG on GPT-4o and said database_.

    #### Future Scope:
    1. Implementation of RAG and Agents on a custom dataset (scapped/collected).
    2. Validation of results via feedback loop of multi LLM agentic framework.
    3. Multi-chat support on the UI.

---

## **Acknowledgement**
Thanks to the open-source libraries and tools used in this project --> OpenAI, Streamlit and On-Demand.<br>
This project was made as a part of the **Alcovia Intern Mandatory Task**. I extend a heartfelt thank you to the Alcovia team for providing me this opportunity.

---

## **License**
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this software, provided proper attribution is given.