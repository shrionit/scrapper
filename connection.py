from sqlalchemy import create_engine
import json
from tools import getConfig


def createEngine():
    config = getConfig()
    database_uri = f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
    return create_engine(database_uri, pool_size=30, max_overflow=10, echo=False)


engine = createEngine()
