import json
import requests

# Grabs question from jService
def get_question():
    response = requests.get("http://jservice.io/api/random")

    # If successful, load as json. Else, return as None
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    else:
        return None
