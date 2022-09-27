 # 

 # 42.74442, 73.67352
 # API URL
 # https://api.ubicquia.com/api
import requests, json
import pdb

token_url = "https://auth.ubihub.ubicquia.com/auth/realms/ubivu-prd/protocol/openid-connect/token"


# Get all Nodes Endpoint
test_api_url = "https://api.ubicquia.com/api/v2/nodes/light"

# Get all alerts Endpoint
#test_api_url = "https://api.ubicquia.com/api/alerts?page=1&per_page=15"

test_api_url = 'https://api.ubicquia.com/api/currentnodestate?isActive=1'

#client (application) credentials on api.ubicquia.com
client_id = '<clientID>'
client_secret = '<SecretKey>'

#step A, B - single call with client credentials as the basic auth header - will return access_token
data = {
    'grant_type': 'client_credentials'
    }

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

print(access_token_response.headers)
print(access_token_response.text)

tokens = json.loads(access_token_response.text)

print("access token: " + tokens['access_token'])

#step B - with the returned access_token we can make as many calls as we want

api_call_headers = {
    'Authorization': 'Bearer ' + tokens['access_token'],
    "accept": "application/json",
    "Content-Type": "application/json"
}

# change method, Accept, and Content-Type below as needed for the respective API endpoint
#api_call_response = requests.post(test_api_url, headers=api_call_headers, verify=False)
api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

print(api_call_response.text)