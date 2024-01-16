import pandas as pd
from streamlit.delta_generator import DeltaGenerator
from models import DBSession

db = DBSession()


def companyList(dg: DeltaGenerator):
    companies = db.getCompany()
    options = list(map(lambda c: c.Name, companies))
    selected = dg.selectbox("Select Company", options=options)
    selected = next(filter(lambda c: c.Name == selected, companies))
    return selected


def getPostCount(companyId):
    count = db.getCompanyPostCount(companyId)
    return count
