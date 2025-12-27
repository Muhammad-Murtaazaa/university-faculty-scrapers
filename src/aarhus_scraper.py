import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from urllib.parse import urljoin
import gender_guesser.detector as gender

# --- Configuration ---
START_URL = "https://cs.au.dk/contact/people"
OUTPUT_FILE = os.path.join("data", "aarhus_staff.csv")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def clean_text(text):
    if text: return " ".join(text.strip().split())
    return ""

def get_gender(full_name, detector):
    """Parses 'Lastname, Firstname' to get 'Firstname' and guesses gender."""
    if not full_name: return "Unknown"

    if "," in full_name:
        name_part = full_name.split(",")[1].strip()
    else:
        name_part = full_name

    first_name = name_part.split()[0].capitalize()
    guess = detector.get_gender(first_name)

    if "female" in guess: return "Female"
    elif "male" in guess: return "Male"
    else: return "Unknown"

def scrape_aarhus():
    d = gender.Detector(case_sensitive=True)
    all_staff_data = []
    seen_ids = set()
    current_url = START_URL
    page_count = 1

    print("--- Starting Aarhus Scraper ---")

    while current_url:
        print(f"Processing Page {page_count}...")
        try:
            response = requests.get(current_url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            person_lists = soup.find_all('div', class_='pure5-persons')

            if person_lists:
                for container in person_lists:
                    # Identify Category
                    category = "Unknown"
                    header_div = container.find_previous('div', class_='csc-header')
                    if header_div and header_div.find('h2'):
                        category = clean_text(header_div.find('h2').text)

                    table = container.find('table', class_='pure-persons-table')
                    if not table: continue

                    rows = table.find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        if not cols: continue

                        # Extract details
                        name_col = cols[0].find('a')
                        name = clean_text(name_col.text) if name_col else clean_text(cols[0].text)
                        
                        profile_link = name_col['href'] if name_col else ""
                        if profile_link and not profile_link.startswith("http"):
                            profile_link = f"https://cs.au.dk{profile_link}"

                        job_title = clean_text(cols[1].text)
                        email_col = cols[2].find('a')
                        email = clean_text(email_col.text) if email_col else clean_text(cols[2].text)
                        phone = clean_text(cols[3].text)
                        mobile = clean_text(cols[4].text)
                        building = clean_text(cols[5].text)

                        # Deduplicate
                        unique_id = email if email else name
                        if unique_id in seen_ids: continue
                        seen_ids.add(unique_id)

                        all_staff_data.append({
                            "Category": category,
                            "Name": name,
                            "Gender": get_gender(name, d),
                            "Job Title": job_title,
                            "Email": email,
                            "Phone": phone,
                            "Mobile": mobile,
                            "Building": building,
                            "Profile Link": profile_link
                        })

            # Find 'Next' link for pagination
            next_link = None
            browse_boxes = soup.find_all('div', class_='tx-pure-pure5-browsebox')
            for box in browse_boxes:
                candidate = box.find('a', string=lambda t: t and "Next" in t)
                if candidate:
                    next_link = candidate['href']
                    break

            if next_link:
                if not next_link.startswith("http"):
                    next_link = urljoin("https://cs.au.dk/", next_link)
                
                if next_link == current_url: break
                current_url = next_link
                page_count += 1
                time.sleep(1)
            else:
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    # Save to CSV
    if all_staff_data:
        headers = ["Category", "Name", "Gender", "Job Title", "Email", "Phone", "Mobile", "Building", "Profile Link"]
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_staff_data)
        
        print(f"SUCCESS! Scraped {len(all_staff_data)} records to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_aarhus()