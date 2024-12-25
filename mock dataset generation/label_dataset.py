import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EXTERNAL_USER_ID = "user"

def get_llm_response(system_query=None, user_query=None):
    create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
    create_session_headers = {
        'apikey': OPENAI_API_KEY
    }
    create_session_body = {
        "pluginIds": [],
        "externalUserId": EXTERNAL_USER_ID
    }

    response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
    response_data = response.json()
    session_id = response_data.get('data', {}).get('id')

    if session_id:
        print("Success!! Session created!")
        if system_query:
            system_prompt_body = {
                "endpointId": "predefined-openai-gpt4o",
                "query": system_query,
                "pluginIds": [],
                "responseMode": "sync",
                "modelConfigs": { "temperature": 0 },
                "role": "system"
            }
        
            system_prompt_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
            system_prompt_headers = {
                'apikey': OPENAI_API_KEY
            }
        
            requests.post(system_prompt_url, headers=system_prompt_headers, json=system_prompt_body)
            print("System prompt made.")
        
        if user_query:
            while True:
                query_body = {
                    "endpointId": "predefined-openai-gpt4o",
                    "query": user_query,
                    "pluginIds": [],
                    "responseMode": "sync",
                    "modelConfigs": { "temperature": 0 }
                }
            
                submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
                submit_query_headers = {
                    'apikey': OPENAI_API_KEY
                }
        
                query_response = requests.post(submit_query_url, headers=submit_query_headers, json=query_body)
                query_response_data = query_response.json()

                if query_response.status_code == 200:
                    print("Query response received")
                    return query_response_data["data"]["answer"]
        
    else:
        print("Failed to create chat session.")

student_attributes = {
    "strenghts":None,
    "weaknessed":None,
    "interests":None,
    "learning_style":None,
    "learning_challenges":None,
    "goals":None,
    "avail":None
}

_format = """{
        "Introduction" : [<Introductory text explaining your understanding of the student>],
        "Workshops" : [<List of workshops>],
        "Activities" : [<List of workshops>],
        "Tasks" : [<List of tasks>],
        "Mentors" : [<List of mentors to connect with their social mdeia links>]
    }
}
"""

SYSTEM_PROMPT = f"""
As an experienced and much loved professor, you are familiar with the problems of multiple students. You have solved a lot of them and helped many of your students become successful.
Some of your key qualities are: Empathetic, polite, knowledgeable, charismatic.

Your task is to understand the problem of the student and provide a comprehensive personalised learning path.

For your understanding, using these attributes a student is defined to you.
**Attrbiutes**:  
1. Strengths
2. Weaknesses
3. Interests
4. Learning Style
5. Learning Challenges
6. Goals
7. Availability

**Description of attribute**:  
1. **Strengths**:Skills or areas where the student naturally excels. These can be academic (specific subjects), extracurricular (arts, sports), or personality traits that contribute to their learning capabilities.
2. **Weaknesses**:Academic-specific areas where the student struggles and needs improvement. These focus on gaps in knowledge or skills within educational contexts.
3. **Interests**:Topics, activities, or fields that the student is naturally curious about or enjoys engaging with. These guide personalized content and motivation.
4. **Learning Style**:Preferences for how a student best absorbs information. Recognizing this helps in presenting content in the most effective way for the learner.
5. **Learning Challenges**:Broader obstacles that impact the student’s ability to learn. These may stem from psychological, physical, or contextual issues.
6. **Goals**:Academic or career aspirations the student hopes to achieve in the short or long term. These guide the direction of the recommended learning path.
7. **Availability**:The amount of time the student can dedicate to learning, along with any scheduling constraints. This helps tailor learning paths to realistic timelines.

**Be specific as much as you can**
"""

if __name__ == "__main__":
    merged_file = "datasets/merged_dataset.json"
    with open(merged_file, "r") as infile:
        students_data = json.load(infile)

    updated_dataset = {}
    count = 0

    for student_id, attributes in students_data.items():
        print(f"Processing {student_id}...")
        USER_PROMPT = f"""
A student has the following characteristics: {student_attributes}. Based on these characteristics, create a detailed study plan tailored to their strengths, weaknesses, interests, and goals. The plan must include:

1. **Workshops**: Recommend the top 5 workshops that align with the student's goals and interests. Provide a brief description and a direct link for each workshop.
2. **Activities**: Suggest activities or extracurricular engagements the student should participate in. These should be relevant to their strengths and interests.
3. **Tasks**: Propose specific tasks such as quizzes, projects, or assignments that will help the student improve in their areas of weakness and achieve their goals.
4. **Mentors**: Recommend at least 3 mentors who can guide the student. Include their names, areas of expertise, and direct links to their LinkedIn, Instagram, or X (formerly Twitter) profiles.

### Format:
Return the study plan in the following structured JSON format:
{_format}

### Constraints:
- Ensure all recommendations are highly relevant and personalized based on the student's attributes.
- Provide URLs for all workshops and mentors where applicable.
- Do not include any extra explanations, commentary, or unrelated information. Only return the structured JSON output.
"""

        response = get_llm_response(SYSTEM_PROMPT, USER_PROMPT)
        if response:
            try:
                response = response.replace("```json", "").replace("```", "").strip()
                study_plan = json.loads(response)
            except json.JSONDecodeError:
                print(f"Invalid JSON response for {student_id}: {response}")
                study_plan = None
        else:
            print(f"No response received for {student_id}")
            study_plan = None

        updated_dataset[student_id] = {
            "attributes": attributes,
            "study_plan": study_plan,
        }

        # time.sleep(0)
        count+=1

        if count%10 == 0:
            output_file = "datasets/refined_final_dataset.json"
            with open(output_file, "w+") as outfile:
                json.dump(updated_dataset, outfile, indent=4)

    print(f"Updated dataset saved to {output_file}.")