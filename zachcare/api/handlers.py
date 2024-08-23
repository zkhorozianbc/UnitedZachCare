from zachcare.db.conn import Session
from typing import Any
from zachcare.db.models import *
from zachcare.db.util import get_or_create_model, get_policy_instance
from zachcare.ml.insurance_model import predict_charges
import random


def calculate_premium(medical_data: dict[str, Any]) -> float:
    """Calculate insurance premium as a factor of predicted yearly charges"""
    predicted_charges = predict_charges(medical_data)
    return predicted_charges / 12.0


def submit_coverage_request(policy_name, row) -> dict[str, Any]:
    with Session.begin() as session:
        medical_condition = get_or_create_model(
            session, MedicalCondition, name=row["medical_history"]
        )
        family_medical_condition = get_or_create_model(
            session, MedicalCondition, name=row["family_medical_history"]
        )
        medical_history = MedicalHistory(
            age=row["age"],
            gender=row["gender"],
            bmi=row["bmi"],
            children=row["children"],
            is_smoker=row["smoker"] == "yes",
            region=row["region"],
            exercise_frequency=row["exercise_frequency"],
            occupation=row["occupation"],
            medical_condition=medical_condition,
            family_medical_condition=family_medical_condition,
        )
        ssn = random.randint(0, 100000)
        customer = Customer(
            name=f"name_{str(ssn)}", ssn=ssn, medical_history=medical_history
        )
        policy_instance = PolicyInstance(
            customer=customer,
            policy=Policy(name=policy_name),
            premium=calculate_premium(row),
        )
        session.add(customer)
        session.add(medical_history)
        session.add(policy_instance)
        session.flush()
        return dict(customer_id=customer.id, premium=policy_instance.premium)


def update_medical_history(customer_id: int, new_medical_data: dict[str, Any]) -> int:
    with Session.begin() as session:
        medical_history = (
            session.query(MedicalHistory).filter_by(customer_id=customer_id).first()
        )
        medical_condition_attrs = {"medical_condition", "family_medical_condition"}
        medical_history_fields = set(medical_history.as_dict().keys()).union(
            medical_condition_attrs
        )
        if set(new_medical_data) - medical_history_fields:
            raise ValueError(
                f"Unknown medical history fields provided: {new_medical_data}"
            )
        for attr, value in new_medical_data.items():
            if attr in medical_condition_attrs:
                medical_condition = get_or_create_model(
                    session, MedicalCondition, name=new_medical_data[attr]
                )
                medical_history.medical_condition = medical_condition
            else:
                setattr(medical_history, attr, value)
        session.flush()
        new_medical_history = medical_history.as_dict()
        premium = calculate_premium(new_medical_history)
        policy_instance = get_or_create_model(
            session, PolicyInstance, customer_id=customer_id
        )
        policy_instance.premium = premium
        return new_medical_history, premium
