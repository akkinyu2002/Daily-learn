import os
import json
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

DATA_FILE = "secure_notes_data.json"


# -------------------------
# Key Derivation
# -------------------------
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    return kdf.derive(password.encode())


# -------------------------
# Encryption
# -------------------------
def encrypt(text: str, password: str):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, text.encode(), None)

    return {
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
    }


def decrypt(enc_data: dict, password: str) -> str:
    salt = base64.b64decode(enc_data["salt"])
    nonce = base64.b64decode(enc_data["nonce"])
    ciphertext = base64.b64decode(enc_data["ciphertext"])

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    decrypted = aesgcm.decrypt(nonce, ciphertext, None)
    return decrypted.decode()


# -------------------------
# Storage
# -------------------------
def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=4)


# -------------------------
# CLI
# -------------------------
def main():
    print("🔐 Secure Notes (Single File Version)")
    password = getpass.getpass("Enter your encryption password: ")

    notes = load_notes()

    while True:
        print("\n1) Create Note")
        print("2) View Notes")
        print("3) Delete Note")
        print("4) Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Title: ")
            print("Enter note content. End with single line: .end")

            lines = []
            while True:
                line = input()
                if line.strip() == ".end":
                    break
                lines.append(line)

            content = "\n".join(lines)

            encrypted = encrypt(content, password)
            notes.append({"title": title, "data": encrypted})
            save_notes(notes)

            print("✅ Note saved securely.")

        elif choice == "2":
            if not notes:
                print("No notes found.")
                continue

            for i, note in enumerate(notes):
                print(f"{i+1}) {note['title']}")

            try:
                index = int(input("Select note number: ")) - 1
                decrypted = decrypt(notes[index]["data"], password)
                print("\n----- NOTE -----")
                print(decrypted)
                print("----------------")
            except Exception:
                print("❌ Wrong password or invalid selection.")

        elif choice == "3":
            for i, note in enumerate(notes):
                print(f"{i+1}) {note['title']}")

            try:
                index = int(input("Delete note number: ")) - 1
                notes.pop(index)
                save_notes(notes)
                print("🗑 Note deleted.")
            except:
                print("Invalid selection.")

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()