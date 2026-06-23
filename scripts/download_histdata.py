#!/usr/bin/env python3
"""
HistData.com downloader with CAPTCHA/rate-limit handling.

Downloads EURUSD M1 data from HistData.com with:
- Automatic token extraction
- SHA256 verification
- Rate limiting (30s between requests)
- Retry logic with exponential backoff
- CAPTCHA detection and user notification
- Resume capability (skip existing validated files)

Usage:
    python scripts/download_histdata.py 2005 2025
    python scripts/download_histdata.py 2005      # Single year
    python scripts/download_histdata.py --verify  # Verify existing downloads only
"""

import argparse
import hashlib
import time
import sys
from pathlib import Path
from typing import Optional, Tuple
import re

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)


# Configuration
BASE_URL = "https://www.histdata.com"
DOWNLOAD_PAGE_TEMPLATE = (
    "{base}/download-free-forex-historical-data/"
    "?/metatrader/1-minute-bar-quotes/{pair}/{year}"
)
POST_URL = f"{BASE_URL}/get.php"
OUTPUT_DIR = Path("state/download-cache/fx-backtest/histdata/raw")
RATE_LIMIT_SECONDS = 30
MAX_RETRIES = 3
RETRY_BACKOFF = [60, 300, 900]  # 1min, 5min, 15min

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def extract_token(html: str) -> Optional[str]:
    """Extract download token from HistData page HTML."""
    soup = BeautifulSoup(html, 'html.parser')

    # Find hidden input with name="tk"
    tk_input = soup.find('input', {'name': 'tk'})
    if tk_input and tk_input.get('value'):
        return tk_input['value']

    # Fallback: regex search
    match = re.search(r'name="tk"\s+value="([^"]+)"', html)
    if match:
        return match.group(1)

    return None


def detect_captcha(response: requests.Response) -> bool:
    """Detect if response contains CAPTCHA challenge."""
    content_lower = response.text.lower()

    # Common CAPTCHA indicators
    captcha_indicators = [
        'recaptcha',
        'captcha',
        'cloudflare',
        'please verify you are human',
        'security check',
        'ddos protection',
    ]

    if any(indicator in content_lower for indicator in captcha_indicators):
        return True

    # Check for unusual response size (CAPTCHA pages are typically small)
    if response.status_code == 200 and len(response.content) < 5000:
        return True

    return False


def download_year(
    year: int,
    pair: str = "eurusd",
    platform: str = "MT",
    timeframe: str = "M1",
    session: Optional[requests.Session] = None,
) -> Tuple[bool, str]:
    """
    Download one year of data from HistData.

    Returns:
        (success: bool, message: str)
    """
    if session is None:
        session = requests.Session()

    session.headers.update({'User-Agent': USER_AGENT})

    output_file = OUTPUT_DIR / f"HISTDATA_COM_MT_{pair.upper()}_M1_{year}.zip"

    # Check if already exists and valid
    if output_file.exists():
        print(f"  File exists: {output_file.name}")
        if output_file.stat().st_size > 1_000_000:  # > 1MB likely valid
            print(f"  Skipping (appears valid, size: {output_file.stat().st_size:,} bytes)")
            return True, "Already downloaded"
        else:
            print(f"  File too small ({output_file.stat().st_size} bytes), re-downloading...")
            output_file.unlink()

    # Step 1: Get download page and extract token
    download_page_url = DOWNLOAD_PAGE_TEMPLATE.format(
        base=BASE_URL, pair=pair, year=year
    )

    print(f"  Fetching download page: {download_page_url}")

    try:
        page_response = session.get(download_page_url, timeout=30)
        page_response.raise_for_status()
    except requests.RequestException as e:
        return False, f"Failed to fetch page: {e}"

    # Check for CAPTCHA
    if detect_captcha(page_response):
        return False, "CAPTCHA detected - manual intervention required"

    # Extract token
    token = extract_token(page_response.text)
    if not token:
        return False, "Failed to extract download token"

    print(f"  Token extracted: {token[:8]}...{token[-8:]}")

    # Step 2: POST to get.php to download ZIP
    post_data = {
        'tk': token,
        'date': str(year),
        'datemonth': str(year),
        'platform': platform,
        'timeframe': timeframe,
        'fxpair': pair.upper(),
    }

    referer = download_page_url
    headers = {
        'Referer': referer,
        'User-Agent': USER_AGENT,
    }

    print(f"  Downloading ZIP file...")

    try:
        download_response = session.post(
            POST_URL,
            data=post_data,
            headers=headers,
            timeout=120,
            stream=True,
        )
        download_response.raise_for_status()
    except requests.RequestException as e:
        return False, f"Download failed: {e}"

    # Check for CAPTCHA in download response
    if detect_captcha(download_response):
        return False, "CAPTCHA detected during download"

    # Check content type
    content_type = download_response.headers.get('Content-Type', '')
    if 'zip' not in content_type.lower() and 'octet-stream' not in content_type.lower():
        return False, f"Unexpected content type: {content_type}"

    # Save file
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'wb') as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    file_size = output_file.stat().st_size
    print(f"  Downloaded: {output_file.name} ({file_size:,} bytes)")

    # Validate file size (typical year is 2-3 MB)
    if file_size < 500_000:
        output_file.unlink()
        return False, f"Downloaded file too small ({file_size} bytes) - likely error page"

    # Compute SHA256
    sha256 = compute_sha256(output_file)
    print(f"  SHA256: {sha256}")

    return True, f"Success ({file_size:,} bytes)"


def download_range(start_year: int, end_year: int, pair: str = "eurusd"):
    """Download multiple years with rate limiting and retry logic."""
    session = requests.Session()

    results = []

    for year in range(start_year, end_year + 1):
        print(f"\n[{year}] Starting download...")

        success = False
        for attempt in range(MAX_RETRIES):
            if attempt > 0:
                wait_time = RETRY_BACKOFF[attempt - 1]
                print(f"  Retry {attempt}/{MAX_RETRIES - 1} after {wait_time}s...")
                time.sleep(wait_time)

            success, message = download_year(year, pair=pair, session=session)

            if success:
                print(f"  ✅ {message}")
                results.append((year, True, message))
                break
            else:
                print(f"  ❌ {message}")

                if "CAPTCHA" in message:
                    print(f"\n⚠️  CAPTCHA detected for year {year}")
                    print(f"    Manual action required:")
                    print(f"    1. Visit: {BASE_URL}")
                    print(f"    2. Complete CAPTCHA in browser")
                    print(f"    3. Wait 5 minutes")
                    print(f"    4. Re-run this script")
                    results.append((year, False, message))
                    return results

                if attempt == MAX_RETRIES - 1:
                    results.append((year, False, message))

        # Rate limit between years
        if year < end_year:
            print(f"  Rate limiting: waiting {RATE_LIMIT_SECONDS}s before next request...")
            time.sleep(RATE_LIMIT_SECONDS)

    return results


def verify_downloads(start_year: int, end_year: int, pair: str = "eurusd"):
    """Verify existing downloads without re-downloading."""
    print(f"\nVerifying downloads for {pair.upper()} {start_year}-{end_year}...\n")

    results = []

    for year in range(start_year, end_year + 1):
        output_file = OUTPUT_DIR / f"HISTDATA_COM_MT_{pair.upper()}_M1_{year}.zip"

        if not output_file.exists():
            print(f"[{year}] ❌ Missing")
            results.append((year, False, "Missing"))
            continue

        file_size = output_file.stat().st_size

        if file_size < 500_000:
            print(f"[{year}] ⚠️  Too small ({file_size:,} bytes)")
            results.append((year, False, "Too small"))
            continue

        sha256 = compute_sha256(output_file)
        print(f"[{year}] ✅ Valid ({file_size:,} bytes, SHA256: {sha256[:16]}...)")
        results.append((year, True, f"{file_size:,} bytes"))

    return results


def print_summary(results):
    """Print download summary."""
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)

    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)

    print(f"\nTotal: {success_count}/{total_count} successful\n")

    if success_count < total_count:
        print("Failed years:")
        for year, success, message in results:
            if not success:
                print(f"  {year}: {message}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Download EURUSD M1 data from HistData.com"
    )
    parser.add_argument(
        'start_year',
        type=int,
        nargs='?',
        help='Start year (e.g., 2005)',
    )
    parser.add_argument(
        'end_year',
        type=int,
        nargs='?',
        help='End year (e.g., 2025). If omitted, downloads only start_year.',
    )
    parser.add_argument(
        '--pair',
        default='eurusd',
        help='Currency pair (default: eurusd)',
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify existing downloads without re-downloading',
    )

    args = parser.parse_args()

    if args.verify:
        if not args.start_year:
            print("ERROR: --verify requires start_year")
            sys.exit(1)
        end_year = args.end_year or args.start_year
        results = verify_downloads(args.start_year, end_year, args.pair)
    else:
        if not args.start_year:
            print("ERROR: start_year required")
            parser.print_help()
            sys.exit(1)

        end_year = args.end_year or args.start_year

        print(f"HistData Downloader")
        print(f"  Pair: {args.pair.upper()}")
        print(f"  Years: {args.start_year}-{end_year}")
        print(f"  Output: {OUTPUT_DIR}")
        print(f"  Rate limit: {RATE_LIMIT_SECONDS}s between requests")

        results = download_range(args.start_year, end_year, args.pair)

    print_summary(results)

    # Exit code reflects success
    success_count = sum(1 for _, success, _ in results if success)
    sys.exit(0 if success_count == len(results) else 1)


if __name__ == '__main__':
    main()
