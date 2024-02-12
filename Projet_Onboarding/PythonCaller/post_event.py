import requests
from datetime import datetime

def get_auth_token(api_base_url, username, password):
    auth_url = f"{api_base_url}api-token-auth/"  
    response = requests.post(auth_url, data={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        raise Exception("Authentification échouée")

def post_event_data(api_base_url, token, events):
    headers = {'Authorization': f'Token {token}'}
    responses = []
    for event in events:
        response = requests.post(f"{api_base_url}post-event/", headers=headers, json=event)
        responses.append({
            'event': event,
            'status_code': response.status_code,
            'response': response.json() if response.status_code == 200 else response.text
        })
    return responses

if __name__ == "__main__":
    API_BASE_URL = "http://localhost:8000/api/" 
    USERNAME = "dima"  
    PASSWORD = "dima"
    TOKEN = get_auth_token(API_BASE_URL, USERNAME, PASSWORD) 

    events = [
        {
            "user": "",
            "user_group" : "iii",
            "event": "ButtonClicked",
            "created": datetime.now().isoformat(),
            "userinfo": "usersystem",
            "feature": "analyse_doc:ChooseDoc",
            "action_type": "CHOOSE"
        },
        {
            "user": "2",
            "user_group" : "iv",
            "event": "PageLoaded",
            "created": datetime.now().isoformat(),
            "userinfo": "usersystem",
            "feature": "analyse_doc:ViewDoc",
            "action_type": "ASKMEYA"
        },
        {
            "user": "1",
            "user_group" : "v",
            "event": "FormSubmitted",
            "created": datetime.now().isoformat(),
            "userinfo": "usersystem",
            "feature": "analyse_doc:SubmitDoc",
            "action_type": "CREATE"
        }
    ]

    event_responses = post_event_data(API_BASE_URL, TOKEN, events)
    for response in event_responses:
        print(f"Event: {response['event']}")
        print(f"Status Code: {response['status_code']}")
        print(f"Response: {response['response']}\n")