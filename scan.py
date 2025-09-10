from collections import deque
from bs4 import BeautifulSoup
from options.header import *
from colors.color import *
import requests
import urllib.parse
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {"User-Agent": "Mozilla/5.0"}

emails = set()
scraped_urls = set()


def get_domain(url):
    """Ambil domain utama dari URL"""
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc


def fetch_url(url, domain_filter):
    """Request & cari email dari 1 URL"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{BOLD_RED}[!] Error saat request {url}: {e}{RESET}")
        return set(), []

    found_emails = set(
        re.findall(r"[a-zA-Z0-9._%+-]+@" + re.escape(domain_filter), response.text)
    )

    soup = BeautifulSoup(response.text, "html.parser")
    links = [
        urllib.parse.urljoin(url, anchor["href"])
        for anchor in soup.find_all("a", href=True)
    ]

    return found_emails, links


def cari_email(target, limit, max_workers=10):
    urls = deque([target])
    count = 0
    domain_filter = get_domain(target)

    global emails, scraped_urls
    emails = set()
    scraped_urls = set()

    try:
        while urls and count < limit:
            batch = []
            while urls and len(batch) < max_workers and count < limit:
                url = urls.popleft()
                if url in scraped_urls:
                    continue
                scraped_urls.add(url)
                batch.append(url)
                count += 1
                print(f"{BOLD_BLUE}[*]{RESET} Memproses {url}")
                time.sleep(0.5)

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_url = {
                    executor.submit(fetch_url, u, domain_filter): u for u in batch
                }
                for future in as_completed(future_to_url):
                    new_emails, new_links = future.result()

                    baru = new_emails - emails
                    if baru:
                        print(f"{BOLD_GREEN}[✓]{RESET} {len(baru)} email baru ditemukan:")
                        for mail in baru:
                            print("   -", mail)

                    emails.update(new_emails)

                    for link in new_links:
                        if (
                            get_domain(link) == domain_filter
                            and link not in urls
                            and link not in scraped_urls
                        ):
                            urls.append(link)

        print(f"\n{BOLD_GREEN}[✓] Scanning selesai.{RESET}")
        print(f"{BOLD_GREEN}[✓]{RESET} Total email ditemukan: {len(emails)}")
        for mail in emails:
            print("  -", mail)

    except KeyboardInterrupt:
        print(f"\n{BOLD_RED}[!] Tools dihentikan...{RESET}")
        time.sleep(0.5)
        sys.exit()


if __name__ == "__main__":
    while True:
        clear_screen()
        header()
        target = input(
            f"{BOLD_BLUE}[?]{RESET} URL target (atau 'exit' untuk keluar): "
        ).strip()
        if target.lower() == "exit":
            print(f"{BOLD_RED}[!] Keluar dari program...{RESET}")
            break

        try:
            limit = int(input(f"{BOLD_BLUE}[?]{RESET} Limit pencarian (misal 10): "))
        except ValueError:
            print(f"{BOLD_RED}[!] Limit harus angka!{RESET}")
            time.sleep(0.5)
            continue

        cari_email(target, limit, max_workers=10)
        print("\n" + "=" * 50)
        lanjut = input(f"{BOLD_BLUE}[?]{RESET} Mau scan lagi? (y/n): ").strip().lower()
        if lanjut != "y":
            print(f"{BOLD_RED}[!] Keluar dari program...{RESET}")
            time.sleep(0.5)
            break
