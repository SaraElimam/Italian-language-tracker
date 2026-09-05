import json
import time
import requests
from bs4 import BeautifulSoup

# URLs provided for all levels
LEVEL_URLS = {
    "A1": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-beginner-level-a1/",
    "A2": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-pre-intermediate-level-a2/",
    "B1": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-intermediate-b1/",
    "B2": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-upper-intermediate-b2/",
    "C1": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-advanced-c1/",
    "C2": "https://onlineitalianclub.com/free-italian-exercises-and-resources/online-italian-course-proficient-c2/"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

IGNORED_SLUGS = [
    "easyreaders", "shop", "faq", "join", "sitemap", 
    "contact", "privacy", "cookies", "best-of", "course-finder",
    "how-to-learn-italian", "online-italian-lessons"
]

all_curriculum = {}

for level, url in LEVEL_URLS.items():
    print(f"Scraping Level {level}...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {level}: {e}")
        continue

    soup = BeautifulSoup(resp.text, "html.parser")
    
    content_area = soup.find("article") or soup.find("div", class_="entry-content") or soup.body

    sections = []
    current_section = {
        "category": f"{level} – Core Lessons & Materials",
        "isScored": False,
        "items": []
    }
    sections.append(current_section)

    for el in content_area.find_all(["h2", "h3", "h4", "p", "ul", "ol"]):
        if el.name in ["h2", "h3", "h4"]:
            heading_text = el.get_text(strip=True)
            
            if heading_text and not any(term in heading_text.lower() for term in ["materials organised", "download", "contact", "need more", "leave a reply", "study checklist"]):
                is_exercise = any(word in heading_text.lower() for word in ["exercise", "quiz", "quizzes", "test"])
                current_section = {
                    "category": heading_text,
                    "isScored": is_exercise,
                    "items": []
                }
                sections.append(current_section)
        
        else:
            for a in el.find_all("a", href=True):
                title = a.get_text(strip=True)
                href = a["href"].split("#")[0].strip()

                if not title or len(title) < 2 or not href.startswith("http"):
                    continue

                if any(slug in href.lower() for slug in IGNORED_SLUGS):
                    continue

                already_exists = any(
                    any(item["url"] == href for item in s["items"]) 
                    for s in sections
                )

                if not already_exists:
                    current_section["items"].append({
                        "title": title,
                        "url": href
                    })

    cleaned_sections = [s for s in sections if len(s["items"]) > 0]
    all_curriculum[level] = cleaned_sections
    
    total_links = sum(len(s["items"]) for s in cleaned_sections)
    print(f"Found {len(cleaned_sections)} sections with {total_links} links for {level}.")
    time.sleep(1)

with open("curriculum.json", "w", encoding="utf-8") as f:
    json.dump(all_curriculum, f, indent=2, ensure_ascii=False)

print("Finished! Saved all levels to curriculum.json")
