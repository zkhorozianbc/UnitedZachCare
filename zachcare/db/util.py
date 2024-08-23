from zachcare.db.conn import Session
from zachcare.db.models import *
from typing import Any

def get_or_create_model(session, model_class, **kwargs):
    model = session.query(model_class).filter_by(**kwargs).first()
    if model is not None:
        return model
    model = model_class(**kwargs)
    session.add(model)
    session.flush()
    return model


def get_customer(**filter_kwargs) -> Customer | None:
    with Session.begin() as session:
        customer = session.query(Customer).filter_by(**filter_kwargs).first()
        return customer.as_dict() if customer else None
    
def get_medical_history(**filter_kwargs) -> MedicalHistory | None:
    with Session.begin() as session:
        medical_history = session.query(MedicalHistory).filter_by(**filter_kwargs).first()
        return medical_history.as_dict()  if medical_history else None

def get_policy_instance(**filter_kwargs) -> PolicyInstance | None:
    with Session.begin() as session:
        policy_instance = session.query(PolicyInstance).filter_by(**filter_kwargs).first()
        return policy_instance.as_dict() if policy_instance else None


        


