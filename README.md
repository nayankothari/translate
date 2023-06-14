# Translation API

url = "http://IP_or_domain/api/translate"

## Installation and Setup project

clone project from github repo: git@github.com:nayankothari/translator.git
install requirement.txt with python -v 3.9.12 using pip3 


## Endpoints

### example using python request module.


# Available languages:

https://en.wikipedia.org/wiki/ISO_639-1
Examples: (e.g. en, ja, ko, pt, zh, zh-TW, ...)

# logs 
will be created in logs directory

# Example with python 
import json
import requests

def get_translation(token):
    """
    This function is use to get translations.
    """
    url = "http://localhost:8000/api/translate"
    query_params = {
        "source_text": "Hello, Nayan Kothari, how are you today ?",
        "source_lang": "en",
        "target_lang": "es"
                }    
    headers = {'Authorization': f'Bearer {token}'}
    print("Request for translations.")
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code == 200:
        data = response.json()        
        translation = data.get("translation")
        print("Translation:", translation)
    else:
        print("Error:", response.status_code)

def get_tokens(username, password):
    """
    This function is use to get refresh and access token.
    """
    url = 'http://localhost:8000/api/token/'        
    data = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}
    print("Request for token.")
    response = requests.post(url, data=json.dumps(data),  headers=headers)    
    # Process the response
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        # refresh_token = token_data['refresh_token']        
        print("Token received.")
        return access_token
        # print(f'Access Token: {access_token}')
        # print(f'Refresh Token: {refresh_token}')
    else:
        print(f'Request failed with status code {response.status_code}')

token = get_tokens(username="nayan", password="nayan")
get_translation(token)
        
