import json, os
from bs4 import BeautifulSoup
import requests


def extract_scripts(element):
    for script in element.find_all("script"):
        if script.has_attr("type") and "application/ld+json" in script.attrs["type"]:
            script_text = script.get_text(strip=True).strip()
            return script_text
    return ""


def read_from_file(file_path):
    try:
        with open(os.path.abspath(file_path), "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading from {file_path.split('/')[-1]}: {e}")
        return None


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


def convert_dict_to_json(input_dict):
    try:
        json_string = json.dumps(input_dict, ensure_ascii=False)
        return json_string
    except Exception as e:
        print(f"Error converting dictionary to JSON: {e}")
        return None
