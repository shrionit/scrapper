import schedule
import time, json
from datetime import datetime, timedelta
from get_latest_linkedin_post import get_latest_linked_post

from models import DBSession, getLastCompanyPosts
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
    companies = get_latest_linked_post(companies)
    for company in companies:
        print(f"CHECKPOINT[{company.Name}]: Got latest post link.")
        postBody = fetchPost(company.latestPostLink)
        print(f"CHECKPOINT[{company.Name}]: Got latest post data.")
        addedpost = db.addCompanyPost(
            company.ID, {"postLink": company.latestPostLink, "postData": postBody}
        )
        if addedpost == "EXISTS":
            print(f"CHECKPOINT[{company.Name}]: Not a new post")
        else:
            print(f"CHECKPOINT[{company.Name}]: Added the post data to db")


def time_until_target(target_seconds):
    current_time = datetime.now()
    target_time = current_time + timedelta(seconds=target_seconds)
    time_difference = target_time - current_time
    seconds_until_target = time_difference.total_seconds()
    return seconds_until_target


def stime(h, m, s):
    return f"{h:02}:{m:02}:{s:02}"


# due to vm being in london time
def main():
    schedule.every().day.at(stime(6, 30, 0)).do(fetchLatestCompanyPost)
    while True:
        schedule.run_pending()
        print("Waiting for next execution", end="\r")
        time.sleep(1)


if __name__ == "__main__":
    main()
