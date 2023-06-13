# Translation API

url = "http://IP_or_domain/api/translate"

## Installation and Setup project

clone project from github repo: git@github.com:nayankothari/translator.git
install requirement.txt with python -v 3.9.12 - pip 

## Endpoints

### example using python request module.
import requests

query_params = {
    "source_text": "Hello, Nayan",
    "source_lang": "en",
    "target_lang": "es"
}

response = requests.get(url, params=query_params)

if response.status_code == 200:
    data = response.json()
    translation = data.get("translation")
    print("Translation:", translation)
else:
    print("Error:", response.status_code)


# Available languages:

https://en.wikipedia.org/wiki/ISO_639-1
Examples: (e.g. en, ja, ko, pt, zh, zh-TW, ...)

# logs 
will be created in logs directory