# File name: hello_client.py
import requests

response = requests.post(
    "http://localhost:8000", json={"language": "spanish", "name": "Dora"}
)
greeting = response.text
print(greeting)

# serve run hello:language_classifier