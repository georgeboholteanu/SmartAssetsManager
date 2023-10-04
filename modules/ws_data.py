# DEPENDENCY FILE FOR MAIN APP
import requests
import time
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

########     LOAD PROJECT ENVIRONMENT VARIABLES      ########
load_dotenv()

# LOGIN TO CLOUD
def login_website():
    # Define the login URL and file download URL
    login_url = f"{os.getenv('auth_url')}"

    # Create a session to retain your login credentials and handle cookies
    session = requests.session()

    # Prepare the login data
    login_data = {
        "_csrf_token": session.cookies.get("__token"),
        "LoginForm[email]": f"{os.getenv('USR')}",
        "LoginForm[password]": f"{os.getenv('PAS')}",
        "LoginForm[rememberMe]": 1,
    }

    # Mimic a web browser by setting appropriate headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": login_url,
    }

    # Add a delay to avoid being flagged as a bot
    time.sleep(5)

    # Send the login POST request with the login data and headers
    login_response = session.post(login_url, data=login_data, headers=headers)

    # Check if the login was successful
    if "Logout" in login_response.text:
        print("Login successful")
        return session
        # Additional actions after successful login
    else:
        print("Login failed")
        # Additional actions when login fails


