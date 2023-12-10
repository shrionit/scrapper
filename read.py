import csv
import json


def read_csv(file_path="Company linkedin URLs - Sheet1.csv"):
    company_list = []
    current_company = None

    with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_name = row.get("Company ")
            linkedin_url = row.get("Company Linkedin")
            post_url = row.get("Posts URL")

            if company_name:
                if current_company:
                    company_list.append(current_company)
                current_company = {
                    "name": company_name,
                    "pageLink": linkedin_url,
                    "postLink": [post_url] if post_url else [],
                }
            elif current_company and post_url:
                current_company["postLink"].append(post_url)

    if current_company:
        company_list.append(current_company)

    return company_list
