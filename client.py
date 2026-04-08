import base64
import getpass
import json
import os
from dataclasses import dataclass
from typing import Optional

import requests
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


API = "http://127.0.0.1:8000"

# -------------------------
# Crypto helpers (client-side)
# -------------------------
def derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    # AESGCM needs 32-byte key for AES-256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt_note(plain_text: str, enc_password: str) -> tuple[bytes, bytes, bytes]:
    salt = os.urandom(16)
    key = derive_key(enc_password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # recommended for GCM
    ciphertext = aesgcm.encrypt(nonce, plain_text.encode("utf-8"), associated_data=None)
    return salt, nonce, ciphertext

def decrypt_note(salt: bytes, nonce: bytes, ciphertext: bytes, enc_password: str) -> str:
    key = derive_key(enc_password, salt)
    aesgcm = AESGCM(key)
    plain = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    return plain.decode("utf-8")

# -------------------------
# API helpers
# -------------------------
def signup(username: str, password: str):
    r = requests.post(f"{API}/signup", json={"username": username, "password": password}, timeout=10)
    if r.status_code not in (200, 201):
        raise SystemExit(f"Signup failed: {r.status_code} {r.text}")
    print("✅ Signup OK")

def login(username: str, password: str) -> str:
    r = requests.post(
        f"{API}/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    if r.status_code != 200:
        raise SystemExit(f"Login failed: {r.status_code} {r.text}")
    token = r.json()["access_token"]
    print("✅ Login OK")
    return token

def list_notes(token: str):
    r = requests.get(f"{API}/notes", headers={"Authorization": f"Bearer {token}"}, timeout=10)
    if r.status_code != 200:
        raise SystemExit(f"List notes failed: {r.status_code} {r.text}")
    notes = r.json()
    if not notes:
        print("(no notes)")
        return
    for n in notes:
        print(f"- id={n['id']}  title={n['title']}  updated={n['updated_at']}")

def create_note(token: str, title: str, plaintext: str, enc_password: str):
    salt, nonce, ciphertext = encrypt_note(plaintext, enc_password)
    payload = {
        "title": title,
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
    }
    r = requests.post(f"{API}/notes", json=_b64_to_bytes_payload(payload), headers={"Authorization": f"Bearer {token}"}, timeout=10)
    if r.status_code != 201:
        raise SystemExit(f"Create failed: {r.status_code} {r.text}")
    print(f"✅ Created note id={r.json()['id']}")

def read_note(token: str, note_id: int, enc_password: str):
    r = requests.get(f"{API}/notes/{note_id}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
    if r.status_code != 200:
        raise SystemExit(f"Read failed: {r.status_code} {r.text}")

    note = r.json()
    salt = base64.b64decode(note["salt"])
    nonce = base64.b64decode(note["nonce"])
    ciphertext = base64.b64decode(note["ciphertext"])
    try:
        plaintext = decrypt_note(salt, nonce, ciphertext, enc_password)
    except Exception:
        raise SystemExit("❌ Decryption failed (wrong encryption password?)")

    print(f"\n=== {note['title']} (id={note['id']}) ===\n{plaintext}\n")

def update_note(token: str, note_id: int, title: str, plaintext: str, enc_password: str):
    salt, nonce, ciphertext = encrypt_note(plaintext, enc_password)
    payload = {
        "title": title,
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
    }
    r = requests.put(
        f"{API}/notes/{note_id}",
        json=_b64_to_bytes_payload(payload),
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    if r.status_code != 200:
        raise SystemExit(f"Update failed: {r.status_code} {r.text}")
    print("✅ Updated")

def delete_note(token: str, note_id: int):
    r = requests.delete(f"{API}/notes/{note_id}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
    if r.status_code != 204:
        raise SystemExit(f"Delete failed: {r.status_code} {r.text}")
    print("✅ Deleted")

def _b64_to_bytes_payload(payload: dict) -> dict:
    # FastAPI expects bytes in JSON as base64-like strings? Actually Pydantic bytes accept base64 in JSON.
    # We'll send as strings, and Pydantic will decode them to bytes.
    return payload


# -------------------------
# CLI
# -------------------------
def main():
    print("Secured Notes CLI")
    print("1) signup  2) login")
    choice = input("Choose: ").strip()

    username = input("Username: ").strip()
    password = getpass.getpass("Login password: ")

    if choice == "1":
        signup(username, password)

    token = login(username, password)

    # Separate encryption password (so server never gets it)
    enc_password = getpass.getpass("Encryption password (used to encrypt/decrypt notes locally): ")

    while True:
        print("\nCommands: list | new | read | update | delete | quit")
        cmd = input("> ").strip().lower()

        if cmd == "list":
            list_notes(token)

        elif cmd == "new":
            title = input("Title: ").strip()
            print("Enter note text. End with a single line: .end")
            lines = []
            while True:
                line = input()
                if line.strip() == ".end":
                    break
                lines.append(line)
            text = "\n".join(lines)
            create_note(token, title, text, enc_password)

        elif cmd == "read":
            note_id = int(input("Note id: ").strip())
            read_note(token, note_id, enc_password)

        elif cmd == "update":
            note_id = int(input("Note id: ").strip())
            title = input("New title: ").strip()
            print("Enter new note text. End with: .end")
            lines = []
            while True:
                line = input()
                if line.strip() == ".end":
                    break
                lines.append(line)
            text = "\n".join(lines)
            update_note(token, note_id, title, text, enc_password)

        elif cmd == "delete":
            note_id = int(input("Note id: ").strip())
            delete_note(token, note_id)

        elif cmd == "quit":
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()