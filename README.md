# 🎓 University Faculty Data Scraper & Analyzer

## Overview
This repository contains two specialized Python scraping pipelines designed to harvest, process, and visualize faculty data from **The University of Pisa (Italy)** and **Aarhus University (Denmark)**.

The project demonstrates advanced web scraping techniques to overcome common challenges such as obfuscated email addresses, hidden internal APIs, and cryptographic pagination tokens.

## 📂 Project Structure

* **`src/`**: Contains the source code for scrapers and visualizers.
* **`data/`**: Stores the raw extracted data in CSV format.
* **`images/`**: Stores the generated statistical dashboards (PNG).

## 🚀 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Muhammad-Murtaazaa/university-faculty-scrapers](https://github.com/Muhammad-Murtaazaa/university-faculty-scrapers)
    cd university-faculty-scrapers
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🛠️ Usage

### 🇮🇹 University of Pisa (Deep-Dive Scraper)
Extracts detailed profile info including publications and courses by querying hidden APIs.

1.  **Run Scraper:**
    ```bash
    python src/pisa_scraper.py
    ```
2.  **Generate Dashboard:**
    ```bash
    python src/pisa_visualizer.py
    ```

### 🇩🇰 Aarhus University (Lightweight Scraper)
Extracts staff directories while handling complex server-side pagination security (`cHash`).

1.  **Run Scraper:**
    ```bash
    python src/aarhus_scraper.py
    ```
2.  **Generate Dashboard:**
    ```bash
    python src/aarhus_visualizer.py
    ```

## 📊 Features
* **Data Enrichment:** Infers gender using `gender-guesser` and `genderize.io`.
* **Anti-Bot Evasion:** Uses randomized delays and realistic headers.
* **Data Cleaning:** Normalizes job titles and extracts building codes.
* **Visual Analytics:** Generates pie charts, bar graphs, and role distribution plots.

## 📝 License
This project is for educational purposes only. Please respect the `robots.txt` of target websites.