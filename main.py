import requests.auth
import json
import os

with open('secrets_secrets.txt', 'r') as f:
    pw = f.readline().strip()
    CLIENT_ID = f.readline().strip()
    SECRET_KEY = f.readline().strip()

# Authenticate App
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
user_agent = 'Sludge/0.0.1'
data = {
    'grant_type': 'password',
    'username': 'Background-Setting-5',
    'password': pw
}
headers = {'User-Agent': user_agent}

# Getting Token Access ID
response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=data, headers=headers)
token_id = " "
if response.status_code == 200:
    token_id = response.json()['access_token']

# Grab a post
OAUTH_ENDPOINT = 'https://oauth.reddit.com'
params_get = {
    'limit': 1
}
headers_get = {
    'User-Agent': user_agent,
    'Authorization': 'Bearer ' + token_id
}
response2 = requests.get(OAUTH_ENDPOINT + '/r/AmItheAsshole/top/', headers=headers_get, params=params_get)
json_data = response2.json()
# appending post data to a json file
# turn this into a for loop when I do more than one post at a time
# check to make sure the file is empty. If it's not, add a comma and newline character to the file
filename = "posts.json"

# read the existing json data
with open(filename, "r") as posts_data:
    existing_data = json.load(posts_data)

# append the new data
existing_data.append(json_data)

# write the updated data back to the file
with open(filename, "a") as posts_data:
    json.dump(existing_data, posts_data, indent=4)
