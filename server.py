from fastapi import FastAPI
from models import DBSession

api = FastAPI()

db = DBSession()

company = "/api/companys"


@api.get(company)
def listCompanies():
    return db.getCompany()


@api.post(company)
def add_company(data: dict):
    if not data:
        return {"error": "Data is required"}

    company_name = data.get("name", None)
    company_link = data.get("link", None)

    if not company_name or not company_link:
        return {"error": "Both 'name' and 'link' are required fields"}

    if db.addCompany({"postLink": company_link, "name": company_name}):
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
