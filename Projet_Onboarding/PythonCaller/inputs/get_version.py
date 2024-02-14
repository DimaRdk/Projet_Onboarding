import requests


def get_auth_token(api_base_url, username, password):
    
    auth_url = f"{api_base_url}api-token-auth/"  
    response = requests.post(auth_url, data={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        raise Exception("Authentification échouée")

def get_project_version(api_base_url, token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f"{api_base_url}version/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return "Erreur lors de la récupération de la version du projet"



if __name__ == "__main__":
    API_BASE_URL = "http://localhost:8000/api/" 
    USERNAME = "dima"  
    PASSWORD = "dima"
    TOKEN = get_auth_token(API_BASE_URL, USERNAME, PASSWORD) 
    version_info = get_project_version(API_BASE_URL, TOKEN)
   
    print(f"Info version: {version_info}")
