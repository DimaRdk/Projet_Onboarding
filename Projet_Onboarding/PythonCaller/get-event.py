import requests
import json
from datetime import datetime
        
def get_auth_token(api_base_url, username, password):
        auth_url = f"{api_base_url}api-token-auth/"  
        response = requests.post(auth_url, data={'username': username, 'password': password})
        if response.status_code == 200:
            return response.json().get('token')
        else:
            raise Exception("Authentification échouée")
    
def get_event_data(api_base_url, token, request_type, user=None, date=None, event=None,action_type= None):
        headers = {'Authorization': f'Token {token}'}
        data = {'request': request_type}
        if action_type:
            data['action_type'] = action_type  
        if user:
            data['user'] = user
        if date:
            data['date'] = date.strftime('%Y-%m-%d')
        if event:
            data['event'] = event
        response = requests.get(f"{api_base_url}get-event/", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erreur lors de la récupération des données d'événement: {response.text}")
    
if __name__ == "__main__":
        API_BASE_URL = "http://localhost:8000/api/" 
        USERNAME = "dima"  
        PASSWORD = "dima"
        TOKEN = get_auth_token(API_BASE_URL, USERNAME, PASSWORD) 
    
        request_type = 'action_type'
        user = None
        date = datetime.now()
        event = None
        action_type = 'CREATE'  
    
        event_data = get_event_data(API_BASE_URL, TOKEN, request_type, user, date, event,action_type)
        print(event_data)