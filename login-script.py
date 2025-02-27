import requests
import json
import re
import uuid

# Load credentials from credentials.json
with open("credentials.json", "r") as file:
    credentials = json.load(file)

login_url = "https://login.texascollege.edu.np/loginpages/userlogin.shtml"
logout_url = "https://login.texascollege.edu.np/loginpages/logout_remote.shtml"
force_login_url = "https://login.texascollege.edu.np/loginpages/logoutusernlogin.shtml"

headers = {
    "Host": "login.texascollege.edu.np",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://login.texascollege.edu.np",
    "Referer": "https://login.texascollege.edu.np/loginpages/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers",
    "Connection": "keep-alive"
}

payload = {
    "username": credentials["username"],
    "password": credentials["password"],
    "termChk": "on"
}

session = requests.Session()
response = session.post(login_url, headers=headers, data=payload)

if response.status_code == 200:
    if "Invalid username or password" in response.text:
        print("Login failed: Invalid username or password.")
    elif "Location: logout_remote.shtml" in response.headers.get("Location", ""):
        print("Redirected to logout page. Attempting forced logout...")

        # Step 1: Fetch logout page to get device details
        logout_params = {
            "uname": credentials["username"] + "@local",
            "original_uid": credentials["username"],
            "custom": "",
            "vidx": "2",
            "utype": "LOCAL"
        }
        logout_response = session.get(logout_url, headers=headers, params=logout_params)

        mac_address_pattern = r'value=\'(.*?)\''
        mac_address_match = re.search(mac_address_pattern, logout_response.text)
        if mac_address_match:
            device_mac = mac_address_match.group(1)
            print(f"Device detected: {device_mac}. Attempting forced login...")

            force_payload = {
                "user": device_mac,
                "mypassword": credentials["password"],
                "textarea": "Seems that your account is already logged in. Supply Credentials to Verify yourself as Authorized User. Need to change your credentials !! Contact IT",
                "myusername": credentials["username"] + "%40local",
                "original_uid": credentials["username"],
                "custom": "",
                "logout": "0",
                "utype": "LOCAL"
            }

            force_response = session.post(force_login_url, headers=headers, data=force_payload)

            if force_response.status_code == 200:
                print("Forced login successful!")
            else:
                print(f"Forced login failed with status code: {force_response.status_code}")
        else:
            print("Failed to retrieve device details for forced login.")
    else:
        print("Login successful!")
else:
    print(f"Login failed with status code: {response.status_code}")

# Save cookies to a file
with open("cookies.txt", "w") as file:
    for cookie in session.cookies:
        file.write(f"{cookie.name}={cookie.value}\n")
