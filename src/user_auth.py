import json
import os
import hashlib

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(username, password, email):
    users = load_users()
    if any(u['username'].lower() == username.lower() for u in users):
        return "Username already exists."

    users.append({
        "username": username,
        "password": hash_password(password),
        "email": email
    })
    save_users(users)
    return "User registered successfully!"

def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    for user in users:
        if user['username'].lower() == username.lower() and user['password'] == hashed:
            return user['username']
    return None
