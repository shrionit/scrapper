import schedule
import time
import json
from get_latest_linkedin_post import get_latest_linked_post

from models import DBSession
from tools import scrape_linkedin_post

companies = None


def fetchPost(postLink):
    try:
        post = scrape_linkedin_post(postLink)
        return post["articleBody"]
    except Exception as e:
        print(post)


def fetchLatestCompanyPost():
    if companies == None:
        db = DBSession()
        companies = db.getCompany()

    for company in companies:
        output = get_latest_linked_post(company.pageLink)
        postBody = fetchPost(output["postLink"])
        db.addCompanyPost(companyId=company.ID, data=postBody)


# due to vm being in london time
schedule.every().day.at("6:30:00").do(fetchLatestCompanyPost)
while True:
    schedule.run_pending()
    time.sleep(60 * 60 * 6)
