# # API Endpoint for authentication
# auth_url = "http://20.244.56.144/evaluation-service/auth"

# # Replace with actual values from your registration response
# auth_data = {
#     "email": "22051850@kiit.ac.in",
#     "name": "Ayush Singh",
#     "rollNo": "22051850",
#     "accessCode": "nwpwrZ",
#     "clientID": "e4c7e42e-eecd-4fbf-8ce2-facbd8c2c953",  # Replace with your generated clientID
#     "clientSecret": "mWbCtyZgkEeCjzdQ"  # Replace with your generated clientSecret
# }

# # Sending the authentication request
# auth_response = requests.post(auth_url, json=auth_data)

# # Checking the response
# if auth_response.status_code == 200:
#     token_info = auth_response.json()
#     print("Authentication Successful! Your Access Token:")
#     print(token_info["access_token"])  # Save this for future API requests
# else:
#     print("Authentication Failed:", auth_response.text)
import requests

# API Endpoint for authentication
auth_url = "http://20.244.56.144/evaluation-service/auth"

# Replace with actual values
auth_data = {
    "email": "22051850@kiit.ac.in",
    "name": "Ayush Singh",
    "rollNo": "22051850",
    "accessCode": "nwpwrZ",
    "clientID": "e4c7e42e-eecd-4fbf-8ce2-facbd8c2c953",  # Replace with your generated clientID
    "clientSecret": "mWbCtyZgkEeCjzdQ"  # Replace with your generated clientSecret
}

# Sending the authentication request
auth_response = requests.post(auth_url, json=auth_data)

# Handling the response properly
if auth_response.status_code in [200, 201]:  # Accept both 200 & 201
    response_json = auth_response.json()
    print("✅ Authentication Successful!")
    print("Access Token:", response_json["access_token"])
else:
    print(f"❌ Authentication Failed: {auth_response.status_code}")
    print(auth_response.text)

