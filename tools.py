import json
from bs4 import BeautifulSoup
import requests


def extract_scripts(element):
    for script in element.find_all("script"):
        if script.has_attr("type") and "application/ld+json" in script.attrs["type"]:
            script_text = script.get_text(strip=True).strip()
            return script_text
    return ""


def create_soup(link):
    response = requests.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return None


def scrape_linkedin_post(linkedin_post_url):
    soup = create_soup(linkedin_post_url)
    if soup:
        scriptcontent = extract_scripts(soup)
        obj = json.loads(scriptcontent)
        return obj
    return None
