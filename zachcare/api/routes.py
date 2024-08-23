from typing import Any
from flask import Flask, request, Response
from zachcare.api.handlers import submit_coverage_request, update_medical_history
from zachcare.db.util import get_customer, get_medical_history, get_policy_instance

app = Flask(__name__)

@app.route("/coverage/request/<policy_name>", methods=["POST"])
def submit_coverage_request_route(policy_name: str) -> Response:
    data = request.get_json()
    coverage_data = submit_coverage_request(policy_name, data)
    return coverage_data


@app.route("/medical_history/<int:customer_id>", methods=["GET", "POST"])
def medical_history_route(customer_id: int):
    customer_data: dict[str, Any] | None = get_customer(id=customer_id)
    if customer_data is None:
        return {"error_msg": f"Customer with id {customer_id} doesn't exist"}
    elif request.method == "GET":
        return get_medical_history(customer_id=customer_data["id"])
    new_medical_data = request.get_json()
    new_medical_history, new_premium = update_medical_history(customer_data["id"], new_medical_data)
    return dict(new_medical_history=new_medical_history, new_premium=new_premium)

@app.route("/customer/<int:customer_id>", methods=["POST"])
def submit_claim(customer_id: int):
    pass

