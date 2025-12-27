import csv
import requests
from bs4 import BeautifulSoup
import time
import os

# --- Configuration ---
MAIN_URL = "https://di.unipi.it/en/people/"
OUTPUT_FILE = os.path.join("data", "unipi_faculty_detailed.csv")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def get_gender(first_name):
    """Determines gender using genderize.io API (cached)."""
    try:
        clean_name = first_name.split()[0]
        url = f"https://api.genderize.io?name={clean_name}&country_id=IT"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['gender'] and data['probability'] > 0.8:
                return data['gender']
    except:
        pass
    return "unknown"

def get_detailed_info(api_url):
    """
    Fetches the specific API url for a person (e.g., work.di.unipi.it/api/persona...)
    and extracts Publications and Courses from the returned JSON/HTML.
    """
    try:
        # The site uses a different domain for the API, so we request it directly
        response = requests.get(api_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json() # The API returns JSON

        # 1. Extract Publications (Field: 'unimap.arpi')
        publications = "N/A"
        if 'unimap' in data and 'arpi' in data['unimap']:
            pub_html = data['unimap']['arpi']
            if pub_html:
                soup_pub = BeautifulSoup(pub_html, 'html.parser')
                pub_list = [li.get_text(strip=True) for li in soup_pub.find_all('li')]
                publications = " ; ".join(pub_list)

        # 2. Extract Courses (Field: 'unimap.insegnamenti')
        courses = "N/A"
        if 'unimap' in data and 'insegnamenti' in data['unimap']:
            course_html = data['unimap']['insegnamenti']
            if course_html:
                soup_course = BeautifulSoup(course_html, 'html.parser')
                course_list = [li.get_text(strip=True) for li in soup_course.find_all('li')]
                courses = " ; ".join(course_list)

        return publications, courses

    except Exception as e:
        return "Error/Empty", "Error/Empty"

def scrape_pisa():
    print(f"Connecting to {MAIN_URL}...")

    try:
        response = requests.get(MAIN_URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Critical Error fetching main page: {e}")
        return

    # Prepare CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'First Name', 'Last Name', 'Gender', 'Email', 'Website', 'Room', 'Phone', 'Recent Publications', 'Courses'])

        rows = soup.find_all('tr', attrs={'data-cat': True})
        total_found = len(rows)
        print(f"Found {total_found} people. Starting detailed extraction...")

        count = 0
        gender_cache = {}

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 6: continue

            # --- Basic Info ---
            category = row['data-cat']
            first_name = cols[0].get_text(strip=True)
            last_name = cols[1].get_text(strip=True)

            # --- Gender (Cached) ---
            name_key = first_name.split()[0].lower()
            if name_key in gender_cache:
                gender = gender_cache[name_key]
            else:
                gender = get_gender(first_name)
                gender_cache[name_key] = gender
                time.sleep(0.1) # Be polite to Gender API

            # --- Email ---
            email_tag = cols[2].find('a', class_='cryptml')
            email = "N/A"
            if email_tag:
                try:
                    name_part = email_tag.get('data-name', '')
                    domain_part = email_tag.get('data-domain', '')
                    tld_part = email_tag.get('data-tld', '')
                    if name_part: email = f"{name_part}@{domain_part}.{tld_part}"
                except: pass

            # --- Website ---
            web_tag = cols[3].find('a')
            website = web_tag['href'] if web_tag and web_tag.has_attr('href') else "N/A"

            # --- Room & Phone ---
            room = cols[4].get_text(strip=True)
            phone = cols[5].get_text(strip=True).replace('tel.', '').strip()

            # --- DETAILED INFO ---
            id_card_tag = cols[6].find('a', class_='openscheda')
            publications = "N/A"
            courses = "N/A"

            if id_card_tag and id_card_tag.has_attr('data-url'):
                api_url = id_card_tag['data-url']
                publications, courses = get_detailed_info(api_url)
                time.sleep(0.2) # Polite delay

            # --- Write to CSV ---
            writer.writerow([category, first_name, last_name, gender, email, website, room, phone, publications, courses])

            count += 1
            print(f"Processed {count}/{total_found}: {first_name} {last_name}")

    print(f"\nDone! Successfully scraped {count} profiles.")
    print(f"Data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_pisa()