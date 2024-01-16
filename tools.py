import json, os
from bs4 import BeautifulSoup
import requests
import tiktoken


def get_token_count(prompt):
    # Use tiktoken to count tokens without making an API call
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoded_text = encoding.encode(prompt)

    return len(encoded_text)


def extract_scripts(element):
    for script in element.find_all("script"):
        if script.has_attr("type") and "application/ld+json" in script.attrs["type"]:
            script_text = script.get_text(strip=True).strip()
            return script_text
    return ""


def getEnv(key, default=None):
    return os.getenv(key, default)


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


def getConfig(configPath="dbconfig.json"):
    config = {}

    try:
        # Try to load config from the file
        with open(os.path.abspath(configPath), "r") as file:
            content = file.read()
            config = json.loads(content)
    except FileNotFoundError:
        # If the file is not found, use environment variables
        config = {
            "username": getEnv("USERNAME"),
            "password": getEnv("PASSWORD"),
            "dbname": getEnv("DBNAME"),
            "port": getEnv("PORT"),
            "host": getEnv("HOST"),
            "lusername": getEnv("LUSERNAME"),
            "lpassword": getEnv("LPASSWORD"),
            "loginWait": getEnv("LOGIN_WAIT"),
            "postPageWait": getEnv("POST_PAGE_WAIT"),
            "postClickWait": getEnv("POST_CLICK_WAIT"),
            "openai_key": getEnv("OPENAI_KEY"),
        }
    return config
