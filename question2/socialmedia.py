import requests
from fastapi import FastAPI, HTTPException
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# FastAPI app
app = FastAPI()

# API Endpoints
BASE_URL = "http://20.244.56.144/evaluation-service"
AUTH_URL = f"{BASE_URL}/auth"
USERS_URL = f"{BASE_URL}/users"

# Credentials
AUTH_DATA = {
    "email": "22051850@kiit.ac.in",
    "name": "Ayush Singh",
    "rollNo": "22051850",
    "accessCode": "nwpwrZ",
    "clientID": "e4c7e42e-eecd-4fbf-8ce2-facbd8c2c953",
    "clientSecret": "mWbCtyZgkEeCjzdQ"
}

# Function to get access token
def get_access_token():
    """Fetches a new access token"""
    try:
        response = requests.post(AUTH_URL, json=AUTH_DATA)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=401, detail="Failed to obtain access token")

        print("✅ Access Token Obtained!")
        return access_token
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching token: {e}")

# Function to get request headers
def get_headers():
    return {"Authorization": f"Bearer {get_access_token()}"}

# Function to fetch posts for a user (Parallel Processing)
def fetch_user_posts(user_id, headers):
    try:
        response = requests.get(f"{USERS_URL}/{user_id}/posts", headers=headers)
        if response.status_code == 200:
            return response.json().get("posts", [])  # Ensure we handle missing keys safely
        return []
    except requests.exceptions.RequestException:
        return []

# Get Top 5 Users with Most Posts (Parallelized)
@app.get("/users")
def get_top_users():
    headers = get_headers()
    
    # Fetch users list
    users_response = requests.get(USERS_URL, headers=headers)
    if users_response.status_code != 200:
        raise HTTPException(status_code=users_response.status_code, detail="Failed to fetch users")
    
    users = users_response.json().get("users", {})  # Ensure fallback
    if not users:
        return {"message": "No users found"}

    # Fetch posts for all users in parallel
    post_counts = Counter()
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda user_id: (user_id, fetch_user_posts(user_id, headers)), users.keys())

    for user_id, posts in results:
        post_counts[user_id] = len(posts)

    # Top 5 users by post count
    top_users = post_counts.most_common(5)
    return {"top_users": [{"user_id": uid, "name": users.get(uid, "Unknown"), "post_count": count} for uid, count in top_users]}

# Get Trending or Latest Posts (More Adaptive)
@app.get("/posts")
def get_posts(type: str):
    """Fetches trending or latest posts dynamically based on API rules"""
    if type not in ["popular", "latest"]:
        raise HTTPException(status_code=400, detail="Invalid type. Choose 'popular' or 'latest'")

    headers = get_headers()
    
    # Fetch users list
    users_response = requests.get(USERS_URL, headers=headers)
    if users_response.status_code != 200:
        raise HTTPException(status_code=users_response.status_code, detail="Failed to fetch users")
    
    users = users_response.json().get("users", {})
    if not users:
        return {"message": "No users found"}

    # Fetch all posts in parallel
    all_posts = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda user_id: fetch_user_posts(user_id, headers), users.keys())

    for posts in results:
        all_posts.extend(posts)

    if not all_posts:
        return {"message": "No posts available"}

    # Dynamic Sorting (Uses API-defined rules)
    if type == "latest":
        sorted_posts = sorted(all_posts, key=lambda x: x.get("id", 0), reverse=True)[:5]
        return {"latest_posts": sorted_posts}

    elif type == "popular":
        comment_counts = Counter()
        with ThreadPoolExecutor() as executor:
            comment_results = executor.map(
                lambda post: (post["id"], requests.get(f"{BASE_URL}/posts/{post['id']}/comments", headers=headers).json().get("comments", [])),
                all_posts
            )

        for post_id, comments in comment_results:
            comment_counts[post_id] = len(comments)

        # Get max comment count dynamically
        max_comments = max(comment_counts.values(), default=0)
        popular_posts = [post for post in all_posts if comment_counts[post["id"]] == max_comments]
        
        return {"popular_posts": popular_posts}

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
