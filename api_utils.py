# api_utils.py
import os, requests, datetime

API_URL      = "http://127.0.0.1:3000"
TOKEN_FILE   = "token.txt"
TOKEN: str | None = None          
CURRENT_USER_EMAIL: str | None = None


def save_token(token: str) -> None:
    """Zapisuje token do pliku i w RAM-ie"""
    global TOKEN
    TOKEN = token           
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def load_token() -> None:
    global TOKEN
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            TOKEN = f.read().strip()

def clear_token() -> None:
    global TOKEN, CURRENT_USER_EMAIL
    TOKEN = None
    CURRENT_USER_EMAIL = None
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def api_post(route: str, **kw):
    return requests.post(f"{API_URL}{route}", **kw)

def api_get(route: str, auth: bool = False, **kw):
    headers = kw.pop("headers", {})
    if auth and TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return requests.get(f"{API_URL}{route}", headers=headers, **kw)
