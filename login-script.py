import requests
import json

with open("credentials.json", "r") as file:
    credentials = json.load(file)

url = "https://login.texascollege.edu.np/loginpages/userlogin.shtml"
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
response = session.post(url, headers=headers, data=payload)

if response.status_code == 200:
    if "Invalid username or password" in response.text:
        print("Login failed: Invalid username or password.")
    elif "You have already logged in" in response.text:
        print("Login failed: User already logged in.")
    else:
        print("Login successful!")
else:
    print(f"Login failed with status code: {response.status_code}")

with open("cookies.txt", "w") as file:
    for cookie in session.cookies:
        file.write(f"{cookie.name}={cookie.value}\n")
