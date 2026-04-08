import json
import os
from getpass import getpass

def load_passwords(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)

def save_passwords(passwords, file_path):
    with open(file_path, 'w') as file:
        json.dump(passwords, file, indent=4)

def add_password(passwords, app_name, username, password):
    if app_name not in passwords:
        passwords[app_name] = []
    passwords[app_name].append({"username": username, "password": password})

def view_passwords(passwords):
    if not passwords:
        print("No passwords stored.")
        return
    for app, creds in passwords.items():
        print(f"App: {app}")
        for cred in creds:
            print(f"  Username: {cred['username']}, Password: {cred['password']}")

def main():
    file_path = "passwords.json"
    passwords = load_passwords(file_path)

    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            app_name = input("Enter the app name: ")
            username = input("Enter the username: ")
            password = getpass("Enter the password: ")
            add_password(passwords, app_name, username, password)
            save_passwords(passwords, file_path)
            print("Password added successfully!")
        elif choice == "2":
            view_passwords(passwords)
        elif choice == "3":
            print("Exiting Password Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()