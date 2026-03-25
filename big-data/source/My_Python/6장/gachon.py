"""
Gachon University SSO Login Script
URL: https://sso.gachon.ac.kr/svc/tk/Auth.do?ac=Y&ifa=N&id=portal

Requirements:
    pip install selenium webdriver-manager

Usage:
    python gachon_login.py
    # Or with credentials as arguments:
    python gachon_login.py --username YOUR_ID --password YOUR_PW
"""

import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

LOGIN_URL = "https://sso.gachon.ac.kr/svc/tk/Auth.do?ac=Y&ifa=N&id=portal"


def get_driver(headless: bool = False) -> webdriver.Chrome:
    """Create and return a Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def login(username: str, password: str, headless: bool = False) -> webdriver.Chrome:
    """
    Log in to Gachon SSO portal.

    Returns the driver (still open) so you can continue automation after login.
    Call driver.quit() when done.
    """
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 15)

    print(f"[*] Opening: {LOGIN_URL}")
    driver.get(LOGIN_URL)

    # ── Wait for the username field ──────────────────────────────────────────
    # Common field names on Korean university SSO portals; adjust if needed.
    possible_id_selectors = [
        (By.ID, "id"),
        (By.NAME, "id"),
        (By.ID, "user_id"),
        (By.NAME, "user_id"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ]

    id_field = None
    for by, selector in possible_id_selectors:
        try:
            id_field = wait.until(EC.presence_of_element_located((by, selector)))
            print(f"[+] Found ID field via ({by}, '{selector}')")
            break
        except Exception:
            continue

    if id_field is None:
        raise RuntimeError("Could not locate the username input field. "
                           "Inspect the page and update the selector.")

    # ── Fill in credentials ──────────────────────────────────────────────────
    id_field.clear()
    id_field.send_keys(username)

    # Password field — try common selectors
    possible_pw_selectors = [
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.ID, "pw"),
        (By.NAME, "pw"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]

    pw_field = None
    for by, selector in possible_pw_selectors:
        try:
            pw_field = driver.find_element(by, selector)
            print(f"[+] Found PW field via ({by}, '{selector}')")
            break
        except Exception:
            continue

    if pw_field is None:
        raise RuntimeError("Could not locate the password input field. "
                           "Inspect the page and update the selector.")

    pw_field.clear()
    pw_field.send_keys(password)

    # ── Submit ───────────────────────────────────────────────────────────────
    # Try clicking a login button first; fall back to Enter key
    possible_btn_selectors = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.ID, "loginBtn"),
        (By.CLASS_NAME, "btn_login"),
        (By.XPATH, "//button[contains(text(),'로그인')]"),
        (By.XPATH, "//a[contains(text(),'로그인')]"),
    ]

    clicked = False
    for by, selector in possible_btn_selectors:
        try:
            btn = driver.find_element(by, selector)
            btn.click()
            print(f"[+] Clicked login button via ({by}, '{selector}')")
            clicked = True
            break
        except Exception:
            continue

    if not clicked:
        print("[!] No login button found — pressing Enter on password field.")
        pw_field.send_keys(Keys.RETURN)

    # ── Wait for navigation ──────────────────────────────────────────────────
    time.sleep(3)  # give the page time to redirect

    current_url = driver.current_url
    print(f"[*] Current URL after login: {current_url}")

    # Basic success check — adjust the expected URL fragment for Gachon portal
    if "Auth.do" not in current_url:
        print("[✓] Login appears successful (redirected away from auth page).")
    else:
        print("[!] Still on auth page — check your credentials or page selectors.")

    return driver


def main():
    parser = argparse.ArgumentParser(description="Gachon SSO Selenium Login")
    parser.add_argument("--username", "-u", help="Student/staff ID")
    parser.add_argument("--password", "-p", help="Password")
    parser.add_argument("--headless", action="store_true",
                        help="Run Chrome in headless mode (no GUI)")
    args = parser.parse_args()

    username = args.username or input("Username: ")
    password = args.password or input("Password: ")

    driver = login(username, password, headless=args.headless)

    # ── Add your post-login automation here ─────────────────────────────────
    # Example: take a screenshot
    driver.save_screenshot("after_login.png")
    print("[*] Screenshot saved to after_login.png")

    input("\nPress Enter to close the browser...")
    driver.quit()


if __name__ == "__main__":
    main()