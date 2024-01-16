import json
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    func,
    desc,
    inspect,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from connection import engine

Base = declarative_base()
inspector = inspect(engine)


class Company(Base):
    __tablename__ = "companies"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    pageLink = Column(String)
    aboutData = Column(Text)
    companyLink = Column(String)
    companyLinkData = Column(Text)

    # Define the relationship to CompanyPost
    posts = relationship(
        "CompanyPost", back_populates="company", cascade="all, delete-orphan"
    )


class CompanyPost(Base):
    __tablename__ = "companyposts"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    postLink = Column(String)
    postData = Column(Text)

    # Define the relationship to Company
    companyId = Column(Integer, ForeignKey("companies.ID"))
    company = relationship("Company", back_populates="posts")


class Prompt(Base):
    __tablename__ = "prompts"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    prompt = Column(Text)


# Check if tables exist
Base.metadata.create_all(bind=engine)


class DBSession:
    def __init__(self):
        self.SessionMaker = sessionmaker(bind=engine)
        self.session = None

    def start(self):
        self.session = self.SessionMaker()

    def close(self):
        if self.session:
            self.session.close()

    def getCompany_prev(self, companyId=None):
        self.start()
        if not companyId:
            companies = self.session.query(Company).all()
        else:
            companies = self.session.query(Company).filter_by(ID=companyId).first()
        self.close()
        return companies

    def getCompany(self, companyId=None):
        self.start()
        out = None
        if not companyId:
            # Fetch all companies and their post counts
            out = []
            companies = (
                self.session.query(
                    Company, func.count(CompanyPost.ID).label("postCount")
                )
                .outerjoin(CompanyPost, Company.ID == CompanyPost.companyId)
                .group_by(Company.ID)
                .all()
            )

            # Now each company in the 'companies' list will have a 'postCount' attribute
            for company, post_count in companies:
                company.postCount = post_count
                out.append(company)

        else:
            # Fetch a specific company and its post count
            company = (
                self.session.query(
                    Company, func.count(CompanyPost.ID).label("postCount")
                )
                .outerjoin(CompanyPost, Company.ID == CompanyPost.companyId)
                .filter(Company.ID == companyId)
                .group_by(Company.ID)
                .first()
            )

            if company:
                company[0].postCount = company[1]
                out = company[0]
            else:
                # Handle the case where the company with the specified ID is not found
                company = None
                out = None

        self.close()
        return out

    def getCompanyPostCount(self, companyId):
        self.start()
        count = self.session.query(CompanyPost).filter_by(companyId=companyId).count()
        self.close()
        return count

    def getCompanyPost(self, companyId, offset=0, limit=10):
        self.start()
        if limit:
            posts = (
                self.session.query(CompanyPost)
                .filter_by(companyId=companyId)
                .order_by(desc(CompanyPost.ID))
                .offset(offset)
                .limit(limit)
            )
        else:
            posts = (
                self.session.query(CompanyPost)
                .filter_by(companyId=companyId)
                .order_by(desc(CompanyPost.ID))
                .all()
            )
        self.close()
        return posts

    def getCompanyPostByLink(self, post_link):
        self.start()
        post = self.session.query(CompanyPost).filter_by(postLink=post_link).first()
        self.close()
        return post

    def filterCompanyByName(self, name):
        self.start()
        out = self.session.query(Company).filter(Company.Name.ilike(f"%{name}%")).all()
        self.close()
        return out

    def deleteCompany(self, companyId):
        self.start()
        self.session.delete(self.session.query(Company).get(companyId))
        self.session.commit()
        self.close()
        return {"message": "Company deleted successfully"}

    def addCompany(self, data):
        self.start()
        Name = data.get("name").strip()
        existing_post = self.session.query(Company).filter_by(Name=Name).first()
        if existing_post:
            print(f"Company with name '{Name}' already exists. Not adding a new one.")
            self.close()
            return "EXISTS"
        else:
            new_company = Company(
                Name=data.get("name"),
                pageLink=data.get("pageLink"),
                aboutData=data.get("aboutData"),
                companyLink=data.get("companyLink"),
                companyLinkData=data.get("companyLinkData"),
            )
            self.session.add(new_company)
            self.session.commit()
            self.close()
            return new_company

    def addCompanyPost(self, companyId, data):
        self.start()

        company = self.session.query(Company).get(companyId)

        if company:
            post_link = data.get("postLink")
            # Check if a post with the same link already exists
            existing_post = (
                self.session.query(CompanyPost).filter_by(postLink=post_link).first()
            )
            if existing_post:
                print(
                    f"Post with link '{post_link}' already exists. Not adding a new one."
                )
                self.close()
                return "EXISTS"
            else:
                new_post = CompanyPost(
                    postLink=post_link,
                    postData=data.get("postData"),
                    company=company,
                )

                self.session.add(new_post)
                self.session.commit()
                self.close()
                return new_post
        else:
            print(f"Company with ID {companyId} not found.")
            self.close()
            return None

    def updateCompanyPost(self, post_id, new_post_data):
        self.start()
        post = self.session.query(CompanyPost).get(post_id)
        if post:
            post.postData = new_post_data
            self.session.commit()
            self.close()
            return post
        else:
            print(f"Company post with ID {post_id} not found.")
            self.close()
            return None

    def updatePostData(self, post_id, new_post_data):
        self.start()
        post = self.session.query(CompanyPost).get(post_id)
        if post:
            post.postData = new_post_data
            self.session.commit()
            self.close()
            return post
        else:
            print(f"Company post with ID {post_id} not found.")
            self.close()
            return None

    def updateCompany(self, companyId, data):
        self.start()
        company = self.session.query(Company).filter_by(ID=companyId).first()
        if company:
            company.pageLink = data.get("pageLink", company.pageLink)
            company.companyLink = data.get("companyLink", company.companyLink)
            company.aboutData = data.get("aboutData", company.aboutData)
            company.companyLinkData = data.get(
                "companyLinkData", company.companyLinkData
            )
            self.session.commit()
        self.close()

    def getPrompts(self, id=None):
        self.start()
        out = None
        if id:
            out = self.session.query(Prompt).filter_by(ID=id).first()
        else:
            out = self.session.query(Prompt).all()
        self.close()
        return out

    def addPrompt(self, prompt):
        self.start()
        prompt = Prompt(prompt=prompt)
        self.session.add(prompt)
        self.session.commit()
        self.session.refresh(prompt)
        self.close()
        return prompt

    def updatePrompt(self, id, newPrompt):
        self.start()
        prompt = self.session.query(Prompt).filter_by(ID=id).first()
        out = None
        if prompt:
            prompt.prompt = newPrompt
            self.session.commit()
            self.session.refresh(prompt)
            out = prompt
        self.close()
        return out

    def deletePrompt(self, id):
        self.start()
        prompt = self.session.query(Prompt).filter_by(ID=id).first()
        out = None
        if prompt:
            self.session.delete(prompt)
            self.session.commit()
            out = {"message": "Prompt deleted successfully"}
        else:
            out = {"Error": "Prompt not found"}
        self.close()
        return out


def getLastCompanyPosts():
    db = DBSession()
    for company in db.getCompany():
        lastPost = db.getCompanyPost(company.ID)[-1]
        lp = {
            "companyName": company.Name,
            "lastPostID": lastPost.ID,
            "postLink": lastPost.postLink,
        }
        print(json.dumps(lp, indent=4))
