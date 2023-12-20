from sqlalchemy import create_engine
import json
from tools import read_from_file


def createEngine():
    configpath = "dbconfig.json"
    config = json.loads(read_from_file(configpath))
    database_uri = f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"
    return create_engine(database_uri, pool_size=30, max_overflow=10, echo=False)


engine = createEngine()
