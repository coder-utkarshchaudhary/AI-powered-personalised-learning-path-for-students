import requests

def get_llm_response(system_query=None, user_query=None, openai_api_key=None, external_user_id=None):
    create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
    create_session_headers = {
        'apikey': openai_api_key
    }
    create_session_body = {
        "pluginIds": [],
        "externalUserId": external_user_id
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
                'apikey': openai_api_key
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
                    'apikey': openai_api_key
                }
        
                query_response = requests.post(submit_query_url, headers=submit_query_headers, json=query_body)
                query_response_data = query_response.json()

                if query_response.status_code == 200:
                    print("Query response received")
                    return query_response_data["data"]["answer"]
        
    else:
        print("Failed to create chat session.")