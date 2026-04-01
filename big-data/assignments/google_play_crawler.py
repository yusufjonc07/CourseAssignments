"""
Google Play Store Review Crawler
Uses Selenium for dynamic page rendering + BeautifulSoup for parsing.

Requirements:
    pip install selenium beautifulsoup4 webdriver-manager pandas

Usage:
    python google_play_crawler.py
    Or import and call: scrape_reviews(app_id, max_reviews, output_csv)
"""



import time
import csv
import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


# ─── Configuration ────────────────────────────────────────────────────────────

APP_ID       = "com.kakao.talk"   # Change to your target app's package name
MAX_REVIEWS  = 200                   # Max reviews to collect (scroll until reached)
OUTPUT_CSV   = "play_reviews.csv"    # Output file name
SCROLL_PAUSE = 2.5                   # Seconds to wait after each scroll
LOAD_TIMEOUT = 15                    # Max seconds to wait for page elements


# ─── Selector Helpers ─────────────────────────────────────────────────────────

def select_review_cards(soup: BeautifulSoup):
    """Return review card elements for old/new Google Play layouts."""
    cards = soup.select("div.RHo1pe")  # Current layout (2026)
    if cards:
        return cards
    return soup.select("div[jscontroller='H6eOGe']")  # Older layout fallback


# ─── Driver Setup ─────────────────────────────────────────────────────────────

def build_driver(headless: bool = True) -> webdriver.Chrome:
    """Create and return a configured Chrome WebDriver."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--lang=en-US")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ─── Page Interaction ─────────────────────────────────────────────────────────

def open_reviews_page(driver: webdriver.Chrome, app_id: str) -> None:
    """Navigate to the app page and open the 'See all reviews' modal."""
    url = f"https://play.google.com/store/apps/details?id={app_id}&hl=en&gl=US"
    print(f"[+] Opening: {url}")
    driver.get(url)

    # Click "See all reviews" button
    try:
        wait = WebDriverWait(driver, LOAD_TIMEOUT)
        see_all_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'See all reviews')]")
            )
        )
        driver.execute_script("arguments[0].click();", see_all_btn)
        print("[+] Opened 'See all reviews' panel")
        time.sleep(2)
    except TimeoutException:
        print("[!] 'See all reviews' button not found — scraping visible reviews only")


def sort_by_newest(driver: webdriver.Chrome) -> None:
    """Switch the review sort order to 'Newest' for fresher data."""
    try:
        wait = WebDriverWait(driver, LOAD_TIMEOUT)
        # New layout: click current sort label (e.g. "Most relevant") then choose "Newest"
        sort_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Most relevant' or normalize-space()='Rating' or normalize-space()='Newest']")
            )
        )
        driver.execute_script("arguments[0].click();", sort_btn)
        time.sleep(0.8)

        newest_opt = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Newest']")
            )
        )
        newest_opt.click()
        print("[+] Sorted by Newest")
        time.sleep(2)
    except (TimeoutException, NoSuchElementException):
        # Fallback to old selector set
        try:
            sort_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Sort reviews by']")
                )
            )
            sort_btn.click()
            time.sleep(1)
            newest_opt = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[@data-value='2']")
                )
            )
            newest_opt.click()
            print("[+] Sorted by Newest")
            time.sleep(2)
        except (TimeoutException, NoSuchElementException):
            print("[!] Could not change sort order — using default")


def scroll_to_load(driver: webdriver.Chrome, target: int) -> None:
    """Scroll the reviews container (or page) until target review count reached."""
    # Try to find the scrollable reviews dialog first
    try:
        container = driver.find_element(
            By.XPATH, "//div[contains(@class,'fysCi') and contains(@class,'Vk3ZVd')]"
        )
    except NoSuchElementException:
        try:
            container = driver.find_element(
                By.XPATH, "//div[@jsname='fk8dgd']"   # older layout fallback
            )
        except NoSuchElementException:
            container = None

    last_count = 0
    stall_attempts = 0

    while True:
        # Count currently loaded reviews
        soup = BeautifulSoup(driver.page_source, "html.parser")
        current_count = len(select_review_cards(soup))
        print(f"[~] Reviews loaded: {current_count}", end="\r")

        if current_count >= target:
            print(f"\n[+] Reached target of {target} reviews")
            break

        if current_count == last_count:
            stall_attempts += 1
            if stall_attempts >= 4:
                print(f"\n[!] No new reviews after {stall_attempts} scrolls — stopping")
                break
        else:
            stall_attempts = 0

        last_count = current_count

        # Scroll the container or the page body
        if container:
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", container
            )
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE)


# ─── Parsing ──────────────────────────────────────────────────────────────────

def parse_reviews(page_source: str) -> list[dict]:
    """Parse review cards from the page HTML and return a list of dicts."""
    soup = BeautifulSoup(page_source, "html.parser")
    cards = select_review_cards(soup)
    reviews = []

    for card in cards:
        try:
            # ── Reviewer name
            name_el = (
                card.select_one("div.X5PpBb")
                or card.select_one("span.X43Kjb")
                or card.select_one("[class*='reviewer']")
            )
            name = name_el.get_text(strip=True) if name_el else "Unknown"

            # ── Rating  (aria-label="Rated X stars out of 5")
            rating = None
            star_el = card.select_one("div[role='img'][aria-label]")
            if star_el:
                m = re.search(r"(\d)", star_el["aria-label"])
                rating = int(m.group(1)) if m else None

            # ── Date
            date_el = card.select_one("span.bp9Aid") or card.select_one("span[class*='date']")
            date = date_el.get_text(strip=True) if date_el else ""

            # ── Review text
            body_el = (
                card.select_one("div.h3YV2d")
                or card.select_one("span[jsname='bN97Pc']")
                or card.select_one("span[class*='review-body']")
            )
            body = body_el.get_text(strip=True) if body_el else ""

            # ── Thumbs up (helpful count)
            helpful_el = (
                card.select_one("div.AJTPZc")
                or card.select_one("div.jUL89d")
                or card.select_one("[class*='helpful']")
            )
            helpful = helpful_el.get_text(strip=True) if helpful_el else "0"

            # ── Developer reply
            reply_el = card.select_one("div.ocpBU") or card.select_one("div[class*='developer-reply']")
            reply = reply_el.get_text(strip=True) if reply_el else ""

            reviews.append({
                "reviewer":       name,
                "rating":         rating,
                "date":           date,
                "review":         body,
                "helpful_count":  helpful,
                "dev_reply":      reply,
                "scraped_at":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

        except Exception as e:
            print(f"[!] Skipped a card due to error: {e}")
            continue

    return reviews


# ─── Output ───────────────────────────────────────────────────────────────────

def save_to_csv(reviews: list[dict], filepath: str) -> None:
    """Write review list to a CSV file."""
    if not reviews:
        print("[!] No reviews to save.")
        return

    fieldnames = ["reviewer", "rating", "date", "review",
                  "helpful_count", "dev_reply", "scraped_at"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)

    print(f"[✓] Saved {len(reviews)} reviews → {filepath}")


# ─── Main Entrypoint ──────────────────────────────────────────────────────────

def scrape_reviews(
    app_id: str      = APP_ID,
    max_reviews: int = MAX_REVIEWS,
    output_csv: str  = OUTPUT_CSV,
    headless: bool   = True,
) -> list[dict]:
    """
    Full pipeline: open Play Store → scroll → parse → save CSV.

    Args:
        app_id:      Android package name  (e.g. 'com.spotify.music')
        max_reviews: How many reviews to try to collect
        output_csv:  Path/name of output CSV file
        headless:    Run Chrome without a visible window

    Returns:
        List of review dicts
    """
    driver = build_driver(headless=headless)
    reviews = []

    try:
        open_reviews_page(driver, app_id)
        sort_by_newest(driver)
        scroll_to_load(driver, max_reviews)

        print("\n[+] Parsing reviews...")
        reviews = parse_reviews(driver.page_source)
        print(f"[+] Parsed {len(reviews)} reviews")

        save_to_csv(reviews, output_csv)

    except Exception as e:
        print(f"[✗] Fatal error: {e}")
        raise

    finally:
        driver.quit()

    return reviews


# ─── Run directly ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    scrape_reviews(
        app_id      = APP_ID,
        max_reviews = MAX_REVIEWS,
        output_csv  = OUTPUT_CSV,
        headless    = True,
    )