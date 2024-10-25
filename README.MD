### [UnitedZachCare](https://github.com/zkhorozianbc/UnitedZachCare)
Health Insurance Cloud Data Architecture for a mock use case of determining insurance premiums
based on customer health data. The high-level components of this architecture are
- Flask API
- Amazon RDS Postgres
- Amazon S3
- Python Client for simulating the business logic (simulate.py)

### System Design
[Entity Diagram](docs/System_Design.png)

### Python Client
This entire architecture is demonstrated by running simulate.py.
This file is a script which calls the Flask API twice, once to submit an insurance coverage
request, and again to update their medical data.

These are the operations that occur when each endpoint is called
- POST /coverage/submit | Request Body: json object of medical data
    1. Create Customer, PolicyInstance, MedicalHistory and MedicalCondition records in the database using SQLAlchemy
    2. Compute the predicted yearly insurance charges based on the customer's medical history
    using the trained Linear Regression Model in zachcare.ml.insurance_model.py
    3. Set the PolicyInstance.premium attribute to the calculated premium 
And for a medical history update

- POST /medical_history/<customer_id> | Request Body: json object of medical data
    1. Update existing Medical History record for the customer based on the new fields
    2. Recalculate Insurance Premium and set new value on the customer's policy instance.
See this workflow in action in the screenshot below
[Simulation](docs/Simulation.png)


### API Design
Flask API, routes can be found at zachcare.api.routes.py. The API is hosted on Amazon EC2 and is properly set up to connect to the Amazon RDS Postgres instance. All API code can be found in the zachcare.api package

### Database Design and ORM
The Database server is a Amazon RDS t2.medium instance. The database objects are created with SQLAlchemy. All DB utility code can be found in the zachcare.db package

### Machine Learning Model
The yearly charges predictive model is a linear regression model trained with scikit-learn on fake insurance charges data found here https://www.kaggle.com/datasets/mirichoi0218/insurance. The model is used by the flask API to update the policy instance premium for a customer when their health data changes. All ML code can be found in the zachcare.ml package


### Further Work
- Incorporate simulated claims data
- Choose a different ML model that is able to incrementally learn from new data
- Better database constraints
