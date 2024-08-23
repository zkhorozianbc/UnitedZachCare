import random

import requests
from zachcare import env
from zachcare.db.models import *
from zachcare.db.models.policy import PolicyName
from typing import Any, get_args
import pandas as pd
from zachcare.ml.insurance_model import get_simulation_data


def simulate_one():
    """Simulates a customer requesting coverage, and then updating their medical history.
    The operations on the backend that will occur for a coverage request are
        1. create Customer, PolicyInstance, MedicalHistory, and MedicalCondition records in the database
        2. Compute the predicted yearly insurance charges based on the customer's medical history
        using the trained Linear Regression Model in zachcare.ml.insurance_model.py
        3. Set the PolicyInstance.premium attribute to the calculated premium
    and for a medical history update
        1. Update existing Medical History record for the customer based on the new fields
        2. Recalculate Insurance Premium and set new value on the customer's policy instance.
    """
    api_endpoint = env["API_ENDPOINT"]
    df = get_simulation_data().head(1)
    data = df.iloc[0].to_dict()
    data["smoker"] = "yes"
    print(">> Submitting Coverage Request")
    response = requests.post(
        api_endpoint + f"/coverage/request/{random.choice(get_args(PolicyName))}",
        json=data,
    )
    response_data = response.json()
    if response.status_code != 200:
        raise ValueError(
            f"Encountered bad status code: {response.status_code} with response: {response_data}"
        )
    print(">> Coverage Request Successfully Submitted:", response_data)
    response = requests.get(
        api_endpoint + f"/medical_history/{str(response_data["customer_id"])}"
    )
    print(">> Current Customer Medical History:", response.json())

    new_medical_data = {
        "is_smoker": False,
        "medical_condition": "Heart Disease",
        "bmi": 35.6,
    }
    print(">> Updating Medical History for customer with new data:", new_medical_data)

    response = requests.post(
        api_endpoint + f"/medical_history/{str(response_data["customer_id"])}",
        json=new_medical_data,
    )
    response_data = response.json()
    print(">> Successfully Updated Medical History.")
    print(">> New Premium:", response_data["new_premium"])
    print(">> New Medical History:", response_data["new_medical_history"])


if __name__ == "__main__":
    simulate_one()
