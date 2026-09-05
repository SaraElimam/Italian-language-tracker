import json
import time
import requests
from bs4 import BeautifulSoup

# Online Italian Club index pages for all six levels
LEVEL_URLS = {
    "A1": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-beginner-level-a1/",
    "A2": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-pre-intermediate-level-a2/",
    "B1": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-intermediate-level-b1/",
    "B2": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-upper-intermediate-level-b2/",
    "C1": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-advanced-level-c1/",
    "C2": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-proficiency-level-c2/"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

all_curriculum = {}

for level, url in LEVEL_URLS.items():
    print(f"Scraping Level {level}...")
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {level}: {e}")
        continue

    soup = BeautifulSoup(resp.text, "html.parser")
    sections = []
    current_section = None

    # Parse headers and link blocks
    for el in soup.find_all(["h3", "h4", "p", "ul"]):
        if el.name in ["h3", "h4"]:
            heading = el.get_text(strip=True)
            # Match section headers related to the course
            if any(k in heading.lower() for k in ["lesson", "listening", "exercise", "grammar", "vocab", level.lower()]):
                current_section = {
                    "category": heading,
                    "isScored": "exercise" in heading.lower() or "quiz" in heading.lower(),
                    "items": []
                }
                sections.append(current_section)
        elif current_section:
            for a in el.find_all("a", href=True):
                title = a.get_text(strip=True)
                href = a["href"]
                # Filter out navigation and shop links
                if title and href.startswith("http") and not any(x in href for x in ["easyreaders", "shop", "faq", "join", "sitemap"]):
                    # Avoid duplicates
                    if not any(item["url"] == href for item in current_section["items"]):
                        current_section["items"].append({
                            "title": title,
                            "url": href
                        })

    # Clean out empty categories
    cleaned_sections = [s for s in sections if len(s["items"]) > 0]
    all_curriculum[level] = cleaned_sections
    print(f"-> Found {len(cleaned_sections)} sections with {sum(len(s['items']) for s in cleaned_sections)} links.")
    time.sleep(1)

with open("curriculum.json", "w", encoding="utf-8") as f:
    json.dump(all_curriculum, f, indent=2, ensure_ascii=False)

print("Finished! Saved all levels to curriculum.json")
