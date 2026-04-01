"""
Simple Google Images crawler (Selenium + BeautifulSoup4).

Requirements:
	pip install selenium beautifulsoup4 webdriver-manager

Usage:
	python assignments/google_image_crawler.py
"""

from __future__ import annotations

import csv
import time
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def build_driver(headless: bool = True) -> webdriver.Chrome:
	options = Options()
	if headless:
		options.add_argument("--headless=new")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--window-size=1280,900")
	options.add_argument("--disable-blink-features=AutomationControlled")
	options.add_argument(
		"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
	)
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option("useAutomationExtension", False)

	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=options)
	driver.execute_script(
		"Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
	)
	return driver


def crawl_google_images(query: str, max_images: int = 50, headless: bool = True) -> list[str]:
	driver = build_driver(headless=headless)
	try:
		url = f"https://www.google.com/search?tbm=isch&q={quote_plus(query)}"
		print(f"[+] Open: {url}")
		driver.get(url)
		time.sleep(2)

		all_links: list[str] = []
		seen = set()
		last_count = 0
		stall = 0

		while True:
			soup = BeautifulSoup(driver.page_source, "html.parser")
			page_text = soup.get_text(" ", strip=True).lower()
			if "unusual traffic" in page_text or "enable javascript" in page_text:
				print("\n[!] Google blocked automation on this request.")
				print("[!] Try running with headless mode off.")
				return all_links[:max_images]

			imgs = soup.select("img")

			for img in imgs:
				src = img.get("src") or img.get("data-src")
				if not src:
					continue
				if not src.startswith("http"):
					continue
				if src in seen:
					continue
				seen.add(src)
				all_links.append(src)

			print(f"[~] Collected: {len(all_links)}", end="\r")

			if len(all_links) >= max_images:
				print(f"\n[+] Reached target: {max_images}")
				return all_links[:max_images]

			if len(all_links) == last_count:
				stall += 1
				if stall >= 3:
					print("\n[!] No more new images found")
					return all_links[:max_images]
			else:
				stall = 0

			last_count = len(all_links)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1.5)

	finally:
		driver.quit()


def save_to_csv(image_urls: list[str], output_csv: str) -> None:
	if not image_urls:
		print("[!] No image URLs to save")
		return

	with open(output_csv, "w", newline="", encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(["index", "image_url"])
		for i, url in enumerate(image_urls, start=1):
			writer.writerow([i, url])

	print(f"[+] Saved {len(image_urls)} URLs -> {output_csv}")


def main() -> None:
	query = input("Search keyword: ").strip()
	if not query:
		print("[!] Search keyword is required")
		return

	max_images_raw = input("How many images? (default 30): ").strip()
	max_images = int(max_images_raw) if max_images_raw else 30

	output_csv = input("Output CSV file (default image_urls.csv): ").strip() or "image_urls.csv"
	headless_raw = input("Headless mode? (y/N): ").strip().lower()
	headless = headless_raw == "y"

	image_urls = crawl_google_images(query=query, max_images=max_images, headless=headless)
	save_to_csv(image_urls, output_csv)


if __name__ == "__main__":
	main()
