from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from zachcare import env
from sqlalchemy.orm import sessionmaker


@lru_cache
def get_sqlalchemy_engine(database: str):
    url = URL.create(
        drivername="postgresql",
        username=env["RDS_USER"],
        host=env["RDS_HOST"],
        database=database,
        password=env["RDS_PASSWORD"],
    )
    engine = create_engine(url, execution_options={"isolation_level": "AUTOCOMMIT"})
    return engine


Session = sessionmaker(get_sqlalchemy_engine("insurance"))
