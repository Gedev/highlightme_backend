import requests
import json

url = "http://localhost:8000/api/"
headers = {
    'Content-Type': 'application/json'
}
data = {
    'wl_report_code': 'VYaL6WJTft3hRbxr'
}

if __name__ == "__main__":
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
