import json
from models import DBSession
from tools import scrape_linkedin_post
from csvreader import csv_to_array_of_dicts

filename = "Company linkedin URLs - Sheet1.csv"

result_array = csv_to_array_of_dicts(filename)


db = DBSession()

cl = db.getCompany()
for c in cl:
    if c.Name == "Geekyants" or c.Name == "Appinventiv":
        alist = list(
            filter(
                lambda x: x["Company"] == c.Name,
                result_array,
            )
        )
        for company in alist:
            print("processing :", c.Name)
            for postLink in company["Posts URL"]:
                postData = scrape_linkedin_post(postLink)["articleBody"]
                result = db.addCompanyPost(
                    c.ID, {"postLink": postLink, "postData": postData}
                )
                if result:
                    print(result)
