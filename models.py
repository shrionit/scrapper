import json
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    MetaData,
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


# Check if tables exist
for table in Base.metadata.sorted_tables:
    if inspector.has_table(table.name, schema="public"):
        # Table exists, no need to create
        continue
    else:
        # Create the table
        table.create(bind=engine)


class DBSession:
    def __init__(self):
        self.SessionMaker = sessionmaker(bind=engine)
        self.session = None

    def start(self):
        self.session = self.SessionMaker()

    def close(self):
        if self.session:
            self.session.close()

    def getCompany(self):
        self.start()
        companies = self.session.query(Company).all()
        self.close()
        return companies

    def getCompanyPost(self, companyId):
        self.start()
        posts = self.session.query(CompanyPost).filter_by(companyId=companyId).all()
        self.close()
        return posts

    def getCompanyPostByLink(self, post_link):
        self.start()
        post = self.session.query(CompanyPost).filter_by(postLink=post_link).first()
        self.close()
        return post

    def deleteCompany(self, companyId):
        self.start()
        self.session.delete(self.session.query(Company).get(companyId))
        self.session.commit()
        self.close()
        return {"message": "Company deleted successfully"}

    def addCompany(self, data):
        self.start()
        new_company = Company(Name=data.get("name"), pageLink=data.get("pageLink"))
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
