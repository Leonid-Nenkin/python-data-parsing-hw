import requests
import json

service = 'https://api.github.com/users/Leonid-Nenkin/repos'
req = requests.get(service)
data = json.loads(req.text)
with open('data.json', 'w') as f:
    json.dump(data, f)
