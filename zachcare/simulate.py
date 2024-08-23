import random

import requests
from zachcare import env
from zachcare.db.models import *
from typing import Any, get_args
from zachcare.db.models import Customer, Policy, PolicyInstance, MedicalCondition, MedicalHistory
from zachcare.db.models.policy import PolicyName
from sqlalchemy import select
from typing import Any, get_args
from zachcare.db.conn import Session
import pandas as pd
from zachcare.ml.insurance_model import load_model, get_simulation_data
    

def simulate():
    api_endpoint = env["API_ENDPOINT"]
    df = get_simulation_data()
    charges: dict[int, float] = {}
    for _, row in df.head(1).iterrows():
        simulated_charges = row["charges"]
        json_payload = row.to_dict()
        del json_payload["charges"]
        row["smoker"] = "yes"
        response = requests.post(
            api_endpoint + f"/coverage/request/{random.choice(get_args(PolicyName))}",
            json=json_payload
        )
        response_data = response.json()
        print(response_data)
        if response.status_code != 200:
            raise ValueError(f"Encountered bad status code: {response.status_code} with response: {response_data}")
        charges[response_data["customer_id"]] = simulated_charges
        response = requests.get(api_endpoint + f"/medical_history/{str(response_data["customer_id"])}")
        print(response.json())
        response = requests.post(
            api_endpoint + f"/medical_history/{str(response_data["customer_id"])}",
            json={"is_smoker": False}
        )
        print(response.json())

    
if __name__ == "__main__":
    simulate()