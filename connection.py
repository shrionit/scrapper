from sqlalchemy import create_engine
import json

from tools import read_from_file


def createEngine():
    config = json.loads(read_from_file("dbconfig.json"))
    database_uri = f"postgresql+psycopg2://{config['username']}:{{config['password']}}@{{config['host']}}:{{config['port']}}/{{config['dbname']}}"
    return create_engine(database_uri, echo=False)


engine = createEngine()
