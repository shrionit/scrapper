from sqlalchemy import create_engine


engine = create_engine(
    "postgresql+psycopg2://postgres:postgrespw@scrapperdb.cfvardkbdrj2.ap-south-1.rds.amazonaws.com:5432/"
)

# Raw SQL query to list all databases in PostgreSQL
conn = engine.connect()
result = conn.exec_driver_sql("SELECT datname FROM pg_database;")

# Fetch and print the list of databases
databases = [row[0] for row in result]
print(databases)
