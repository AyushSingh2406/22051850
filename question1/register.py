import requests

# API Endpoint
url = "http://20.244.56.144/evaluation-service/register"

# Your details (Replace with actual values)
data = {
    "email": "22051850@kiit.ac.in",
    "name": "Ayush Singh",
    "mobileNo": "9062980386",  # Replace with your phone number
    "githubUsername": "AyushSingh2406",
    "rollNo": "22051850",
    "collegeName": "KIIT University",
    "accessCode": "nwpwrZ"
}

# Sending the POST request
response = requests.post(url, json=data)

# Checking the response
if response.status_code == 200:
    print("Registration Successful! Save these credentials:")
    print(response.json())  # Contains clientID and clientSecret
else:
    print("Registration Failed:", response.text)
