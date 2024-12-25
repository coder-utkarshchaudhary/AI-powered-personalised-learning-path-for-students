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

student_attributes = ["Strenghts", "Weaknesses", "Interests", "Learning Style", "Learning Challenges", "Goals", "Availability"]

_format = """{
    "student_id": {
        "Strengths": ["<strong_areas>"],
        "Weaknesses": ["<areas_for_improvement>"],
        "Interests": ["<list_of_interests>"],
        "Learning Style": "<learning_style>",
        "Learning Challenges": ["<list_of_challenges_faced>"],
        "Goals": ["<list_of_goals>"],
        "Availability": "<availability_in_hours_or_days>"
    }
}
"""

USER_PROMPT = f"""
Attributes: {student_attributes}

Generate a mock dataset of 10 students based on the these attributes. Keep the list of features corresponding to each attribute 3-5 elements long. Format the dataset in the form of a JSON as shown in the example.
Format: {_format}

Return only a formatted JSON and don't include and explanation.
"""

SYSTEM_PROMPT = f"""
You are an experienced professor who has been in contact with multiple students and know everything about student life and academic plans made by the students. Your goal is to generate a mock dataset of students with their attributes.

**Attrbiutes**:  
1. Strengths
2. Weaknesses
3. Interests
4. Learning Style
5. Learning Challenges
6. Goals
7. Availability

**Descriptions**:  
1. **Strengths**:Skills or areas where the student naturally excels. These can be academic (specific subjects), extracurricular (arts, sports), or personality traits that contribute to their learning capabilities.
2. **Weaknesses**:Academic-specific areas where the student struggles and needs improvement. These focus on gaps in knowledge or skills within educational contexts.
3. **Interests**:Topics, activities, or fields that the student is naturally curious about or enjoys engaging with. These guide personalized content and motivation.
4. **Learning Style**:Preferences for how a student best absorbs information. Recognizing this helps in presenting content in the most effective way for the learner.
5. **Learning Challenges**:Broader obstacles that impact the student’s ability to learn. These may stem from psychological, physical, or contextual issues.
6. **Goals**:Academic or career aspirations the student hopes to achieve in the short or long term. These guide the direction of the recommended learning path.
7. **Availability**:The amount of time the student can dedicate to learning, along with any scheduling constraints. This helps tailor learning paths to realistic timelines.


Some examples are as follows, you can add more if you want:
1. **Strengths**:
- Strong analytical skills and quick at solving puzzles.
- Excels in creative writing and storytelling.
- Good grasp of mathematical concepts.
- Strong interpersonal skills, enjoys group discussions.

2. **Weaknesses**
- Finds grammar rules difficult to remember.
- Struggles with solving word problems in mathematics.
- Poor retention of historical dates and events.
- Weak vocabulary in English or another language.

3. **Interests**
- Interested in astronomy and space exploration.
- Loves playing and designing video games.
- Curious about environmental science and sustainability.
- Enjoys learning about different cultures and languages.

4. **Learning Style**
- Visual: Prefers diagrams, charts, and videos for understanding.
- Auditory: Learns best through lectures, podcasts, or discussions.
- Kinesthetic: Needs hands-on activities like experiments or building projects.
- Reading/Writing: Enjoys learning through textbooks, notes, and written assignments.

5. **Learning Challenges**
- Short attention span, difficulty staying focused.
- Struggles with abstract concepts like theoretical physics or algebra.
- Dyslexia or other learning disabilities affecting reading comprehension.
- Overwhelmed by too many tasks or concepts presented at once.

6. **Goals**
- Wants to improve grades in science to pursue medicine.
- Aspires to become a software engineer and learn coding.
- Aims to secure admission to a prestigious college.
- Short-term goal: Complete an online course in graphic design.

7. **Availability**
- Available for 2 hours daily on weekdays after school.
- Can dedicate weekends entirely to project-based learning.
- Busy with extracurricular activities on Tuesdays and Thursdays.
- Prefers short, 30-minute sessions due to a packed schedule.
"""

if __name__ == "__main__":
    for i in range(30):
        response = get_llm_response(system_query=SYSTEM_PROMPT, user_query=USER_PROMPT)
        response = response.replace("```json", "").replace('```', '')
        # print(response)
        try:
            resp = json.loads(response)
            with open(f'datasets/dataset_{i+1}.json', 'w') as f:
                json.dump(resp, f)
            print(f"Dataset {i+1} created and saved successfully.")
            time.sleep(5)
        except:
            time.sleep(5)
            print(f"Failed iteration {i+1}. Continuing....")
            continue