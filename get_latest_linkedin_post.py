import json
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time

from tools import read_from_file


def scrollToBottom(handle):
    # Set parameters for scrolling through the page
    SCROLL_PAUSE_TIME = 1.5
    MAX_SCROLLS = False
    last_height = handle.execute_script("return document.body.scrollHeight")
    scrolls = 0
    no_change_count = 0

    # Scroll through the page until no new content is loaded
    while True:
        handle.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = handle.execute_script("return document.body.scrollHeight")
        no_change_count = no_change_count + 1 if new_height == last_height else 0
        if no_change_count >= 3 or (MAX_SCROLLS and scrolls >= MAX_SCROLLS):
            break
        last_height = new_height
        scrolls += 1


def createClassSelector(classname):
    return ".".join(f".{classname}".split(" "))


def get_latest_linked_post(pageUrl: str):
    config = json.loads(read_from_file("dbconfig.json"))
    username = config["lusername"]
    password = config["lpassword"]
    loginwait = int(config.get("loginWait", 5))
    postpagewait = int(config.get("postPageWait", 10))
    clickWait = int(config.get("postClickWait", 5))

    # chromeOptions = Options()
    # chromeOptions.add_argument("--no-sandbox")
    # chromeOptions.add_argument("--headless")
    # chromeOptions.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver for Chrome
    browser = webdriver.Chrome()

    # Open LinkedIn login page
    browser.get("https://www.linkedin.com/login")

    # Enter login credentials and submit
    elementID = browser.find_element(By.ID, "username")
    elementID.send_keys(username)
    elementID = browser.find_element(By.ID, "password")
    elementID.send_keys(password)
    elementID.submit()
    time.sleep(loginwait)

    # Navigate to the posts page of the company
    company_name = (
        pageUrl.split("company")[-1].strip("/").split("/")[0].replace("-", " ").title()
    )
    post_page = pageUrl + "/posts"
    post_page = post_page.replace("//posts", "/posts")
    browser.get(post_page)

    time.sleep(postpagewait)

    element = browser.find_element(
        By.CSS_SELECTOR,
        createClassSelector(
            "feed-shared-control-menu__trigger artdeco-button artdeco-button--tertiary artdeco-button--muted artdeco-button--1 artdeco-button--circle artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view"
        ),
    )
    element.click()
    time.sleep(clickWait)
    dropDownContainerClass = createClassSelector(
        "feed-shared-control-menu__content artdeco-dropdown__content artdeco-dropdown--is-dropdown-element artdeco-dropdown__content--has-arrow artdeco-dropdown__content--arrow-right artdeco-dropdown__content--justification-right artdeco-dropdown__content--placement-bottom ember-view"
    )
    dropdown = browser.find_element(By.CSS_SELECTOR, dropDownContainerClass)

    dropdown.find_element(
        By.CSS_SELECTOR,
        createClassSelector("feed-shared-control-menu__item option-share-via"),
    ).click()
    time.sleep(2)
    copied_text = pyperclip.paste()
    return {"companyName": company_name, "postLink": copied_text}


if __name__ == "__main__":
    d = get_latest_linked_post("https://www.linkedin.com/company/accenture/")
    with open("/tmp/out.txt", "w") as f:
        f.writelines(json.dumps(d))
