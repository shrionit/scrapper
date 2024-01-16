from typing import Optional
from get_latest_linkedin_post import get_about_data, scrapPage
from models import DBSession
from ai import AI
from fastapi import FastAPI, Path, Body, Query
from fastapi.responses import PlainTextResponse

from tools import create_soup

api = FastAPI()

db = DBSession()

company = "/api/companys"
prompt = "/api/prompts"

def generateReportFromCompanyData(companyId, limit=10, offset=0, newPrompt=None):
    ai = AI()
    try:
        posts = [
            post.postData
            for post in db.getCompanyPost(companyId, limit=limit, offset=offset)
        ]
        company = db.getCompany(companyId=companyId)
        if not company:
            return f"Error: Company with {companyId=} not found"
        return ai.generateReportFromPosts(
            posts,
            newPrompt,
            aboutData=company.aboutData or "",
            webPageData=company.companyLinkData or "",
        )
    except Exception as e:
        print(f"error: {e}")
        return "Error: Something went wrong with the AI"


@api.get(company)
def listCompanies():
    return db.getCompany()


@api.options(company)
def add_company_options():
    out = {
        "name": "string",
        "link": "string",
        "companyLink": "string",
    }
    return out


@api.post(company)
def add_company(data: dict):
    if not data:
        return {"error": "Data is required"}

    company_name = data.get("name", None)
    company_link = data.get("link", None)
    company_website_link = data.get("companyLink", "")

    aboutData = get_about_data(company_link)
    companyWebData = scrapPage(company_website_link)

    if not company_name or not company_link:
        return {"error": "Both 'name' and 'link' are required fields"}

    payload = {
        "pageLink": company_link,
        "name": company_name,
        "aboutData": aboutData,
        "companyLink": company_website_link,
        "companyLinkData": companyWebData,
    }

    if db.addCompany(payload):
        return {
            "message": "Company added successfully",
            "name": company_name,
            "link": company_link,
        }
    else:
        return "Error: Failed to add company"


@api.delete(company + "/{companyId}")
def deleteCompany(companyId: int):
    out = db.deleteCompany(companyId)
    if out:
        return out
    return "Error: Something went wrong"


@api.get(company)
def searchCompany(name: str = ""):
    return db.filterCompanyByName(name)


@api.get(company + "/{companyId}/insights", response_class=PlainTextResponse)
def getInsights(
    companyId=Path(...),
    limit: Optional[int] = Query(10),
    offset: Optional[int] = Query(0),
    data: Optional[dict] = Body({}),
):
    return generateReportFromCompanyData(
        companyId, limit=limit, offset=offset, newPrompt=data.get("newPrompt", None)
    )


@api.get(prompt)
def getPrompts():
    return db.getPrompts()


@api.get(prompt + "/{promptId}")
def getPrompt(promptId=Path(...)):
    return db.getPrompts(promptId)


@api.post(prompt)
def addPrompt(data: dict):
    prompt = data.get("prompt", None)
    if prompt:
        return db.addPrompt(data.get("prompt"))
    else:
        return {"prompt": "Is Required"}


@api.put(prompt + "/{promptId}")
def updatePrompt(promptId=Path(...), data=Body({})):
    prompt = data.get("prompt", None)
    if prompt:
        return db.updatePrompt(promptId, data.get("prompt"))
    else:
        return {"prompt": "Is Required"}


@api.delete(prompt + "/{promptId}")
def deletePrompt(promptId=Path(...)):
    return db.deletePrompt(promptId)
