import schedule
import time
from datetime import datetime, timedelta
from get_latest_linkedin_post import get_latest_linked_post

from models import DBSession
from tools import scrape_linkedin_post

companies = []


def fetchPost(postLink):
    try:
        post = scrape_linkedin_post(postLink)
        return post["articleBody"]
    except Exception as e:
        print(post)


def fetchLatestCompanyPost():
    global companies
    if len(companies) == 0:
        db = DBSession()
        companies = db.getCompany()
    for company in companies:
        output = get_latest_linked_post(company.pageLink)
        print(f"CHECKPOINT[{output['companyName']}]: Got latest post link.")
        postBody = fetchPost(output["postLink"])
        print(f"CHECKPOINT[{output['companyName']}]: Got latest post data.")
        db.addCompanyPost(company.ID, postBody)
        print(f"CHECKPOINT[{output['companyName']}]: Added the post data to db")


def time_until_target(target_seconds):
    current_time = datetime.now()
    target_time = current_time + timedelta(seconds=target_seconds)
    time_difference = target_time - current_time
    seconds_until_target = time_difference.total_seconds()
    return seconds_until_target


# due to vm being in london time
schedule.every().day.at("07:50:00").do(fetchLatestCompanyPost)
while True:
    schedule.run_pending()
    print("Waiting for next execution")
    time.sleep(1)
