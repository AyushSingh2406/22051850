import requests

# API Endpoints
AUTH_URL = "http://20.244.56.144/evaluation-service/auth"
USERS_URL = "http://20.244.56.144/evaluation-service/users"

auth_data = {
    "email": "22051850@kiit.ac.in",
    "name": "Ayush Singh",
    "rollNo": "22051850",
    "accessCode": "nwpwrZ",
    "clientID": "e4c7e42e-eecd-4fbf-8ce2-facbd8c2c953",  # Replace with your generated clientID
    "clientSecret": "mWbCtyZgkEeCjzdQ"  # Replace with your generated clientSecret
}
try:
    auth_response = requests.post(AUTH_URL, json=auth_data)
    auth_response.raise_for_status()  

    token_data = auth_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        print("❌ Failed to get access token")
        exit()

    print(" Access Token Obtained!")

except requests.exceptions.RequestException as e:
    print(f" Error fetching token: {e}")
    exit()

headers = {"Authorization": f"Bearer {access_token}"}

try:
    users_response = requests.get(USERS_URL, headers=headers)
    users_response.raise_for_status()  

    users = users_response.json()
    print("Users Fetched Successfully!")
    print(users)

except requests.exceptions.HTTPError as http_err:
    if users_response.status_code == 401:
        print("❌ Unauthorized! Check your access token.")
    elif users_response.status_code == 404:
        print("❌ API endpoint not found. Check the URL.")
    else:
        print(f"❌ HTTP Error: {http_err}")

except requests.exceptions.RequestException as e:
    print(f"❌ Failed to fetch users: {e}")
