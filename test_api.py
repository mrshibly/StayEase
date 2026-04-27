import requests
import json

url = "http://127.0.0.1:8000/api/chat/test_session_1/message"
payload = {"message": "I need a room in Sylhet for 3 nights for 2 guests"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
