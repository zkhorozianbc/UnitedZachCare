import sys
from zachcare.db.conn import Session, get_sqlalchemy_engine
from sqlalchemy import text
from zachcare.db.models.base import Base
from zachcare import env
from typing import get_args
from zachcare.db.models import *
from zachcare.db.models.policy import PolicyName


def create_insurance_db():
    """Create postgres database in RDS instance"""
    engine = get_sqlalchemy_engine("postgres")
    with engine.connect() as conn:
        conn.execute(text(f"drop database if exists {env['RDS_DB']}"))
        conn.execute(text(f"create database {env['RDS_DB']}"))


def create_insurance_tables():
    """Create database assets including tables, constraints, and keys
    for the SQLAlchemy models defined on the Base class
    """
    engine = get_sqlalchemy_engine("insurance")
    Base.metadata.create_all(engine)


def create_policies():
    """Insert mock data for insurance policies"""
    policies = []
    for policy_name in get_args(PolicyName):
        policies.append(Policy(name=policy_name))
    with Session.begin() as session:
        session.add_all(policies)


if __name__ == "__main__":
    create_insurance_db()
    create_insurance_tables()
    create_policies()
