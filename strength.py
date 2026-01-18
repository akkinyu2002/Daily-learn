import tkinter as tk
import re
import random
import string
import math

# ---------- Password Strength Logic ----------
def password_strength(password):
    score = 0
    length = len(password)

    # Length scoring
    if length >= 8:
        score += min(40, length * 2)  # up to 40 points

    # Character variety
    if re.search(r'[a-z]', password):
        score += 10
    if re.search(r'[A-Z]', password):
        score += 10
    if re.search(r'[0-9]', password):
        score += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        score += 20

    # Common patterns penalty
    common_patterns = ["password", "1234", "qwerty", "abcd"]
    for pat in common_patterns:
        if pat in password.lower():
            score -= 20

    # Clamp score
    score = max(0, min(100, score))

    # Strength label
    if score < 40:
        strength = "WEAK ❌"
    elif score < 70:
        strength = "MEDIUM ⚠️"
    else:
        strength = "STRONG ✅"

    return strength, score


# ---------- Crack Time Estimator ----------
def crack_time(password):
    length = len(password)
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset += 32  # approx special chars

    if charset == 0:
        return "Instant"

    combinations = charset ** length
    guesses_per_second = 1e9  # 1 billion guesses/sec
    seconds = combinations / guesses_per_second

    # Convert to human-readable
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds/86400)} days"
    else:
        return "Years+"


# ---------- Password Generator ----------
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    # Ensure at least one of each type
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    password += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(password)
    return ''.join(password)


# ---------- GUI ----------
def check_strength():
    pwd = entry.get()
    strength, score = password_strength(pwd)
    time = crack_time(pwd)
    lbl_strength.config(text=f"Strength: {strength}")
    lbl_score.config(text=f"Score: {score}/100")
    lbl_time.config(text=f"Estimated Crack Time: {time}")

def strengthen_input():
    pwd = entry.get()
    if not pwd:
        pwd = generate_password(20)
    else:
        # Shuffle existing characters
        chars = list(pwd)
        random.shuffle(chars)
        
        # Add some complexity if missing
        if not re.search(r'[0-9]', pwd):
            chars.append(random.choice(string.digits))
        if not re.search(r'[^a-zA-Z0-9]', pwd):
            chars.append(random.choice(string.punctuation))
        if not re.search(r'[A-Z]', pwd):
            chars.append(random.choice(string.ascii_uppercase))
            
        random.shuffle(chars) # Shuffle again after adding new chars
        pwd = "".join(chars)
        
    entry.delete(0, tk.END)
    entry.insert(0, pwd)
    check_strength()

def copy_clipboard():
    root.clipboard_clear()
    root.clipboard_append(entry.get())

def toggle_visibility():
    if entry.cget('show') == '*':
        entry.config(show='')
        btn_view.config(text="Hide Password")
    else:
        entry.config(show='*')
        btn_view.config(text="View Password")

root = tk.Tk()
root.title("🔐 Password Strength & Safety Analyzer")
root.geometry("400x300")

entry = tk.Entry(root, width=30, show="*")
entry.pack(pady=5)

btn_view = tk.Button(root, text="View Password", command=toggle_visibility)
btn_view.pack(pady=2)

btn_check = tk.Button(root, text="Check Strength", command=check_strength)
btn_check.pack(pady=5)

lbl_strength = tk.Label(root, text="Strength: ")
lbl_strength.pack()
lbl_score = tk.Label(root, text="Score: ")
lbl_score.pack()
lbl_time = tk.Label(root, text="Estimated Crack Time: ")
lbl_time.pack()

btn_generate = tk.Button(root, text="Strengthen & Shuffle", command=strengthen_input)
btn_generate.pack(pady=10)

btn_copy = tk.Button(root, text="Copy to Clipboard", command=copy_clipboard)
btn_copy.pack(pady=5)

root.mainloop()