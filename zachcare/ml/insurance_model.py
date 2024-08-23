from typing import Any
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os
import numpy.typing as npt
from functools import lru_cache
from zachcare import env


LOCAL_DATA_FOLDER = "./zachcare/data"
SIMULATION_DATA_FILE_PATH = f"{LOCAL_DATA_FOLDER}/simuation_data.csv"
MODEL_FILE_PATH = f"{LOCAL_DATA_FOLDER}/model.pickle"


def get_insurance_data_from_s3() -> pd.DataFrame:
    """ Read data csv from s3. persist a small chunk of the data
    to a csv to ingest later by the mock client that will 
    call the trained model.
    """
    os.environ["AWS_PROFILE"] = "nyu-dbms-iam-user"
    df = pd.read_csv(env["S3_FILE_PATH"])
    return df

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """ Convert dataframe with categorical columns into a new dataframe
    with one column per distinct value per category to use for regression model
    """
    data_cols = {}
    for col,dtype in sorted(df.dtypes.to_dict().items()):
        if dtype != 'object':
            data_cols[col] = df[col]
        else:
            df_dummy = pd.get_dummies(df[col], col).apply(lambda series: pd.Categorical(series, ordered=True).codes)
            for dummy_col in df_dummy.columns:
                data_cols[dummy_col] = df_dummy[dummy_col]
    processed_df = pd.DataFrame(data_cols)
    return processed_df

def train_model(df: pd.DataFrame) -> LinearRegression:
    """ Train a linear model using stochastic gradient descent. Returns model to be pickled
    and later loaded for predictions.
    """
    target_variable = "charges"
    X,y = df.drop(columns=[target_variable]), df[target_variable]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Finished training model!")

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    return model


def save_model(model: LinearRegression, model_file_path: str = MODEL_FILE_PATH) -> None:
    """Save model on disk in pickled format"""
    with open(model_file_path, 'wb') as model_file:
        pickle.dump(model, model_file)

@lru_cache
def load_model(model_file_path: str = MODEL_FILE_PATH) -> LinearRegression:
    """Load model from disk using pickle"""
    with open(model_file_path, 'rb') as model_file:
        return pickle.load(model_file)
        
def get_feature_columns(model: LinearRegression | None = None) -> list[str]:
    if model is None:
        model = load_model()
    return list(model.feature_names_in_)

def get_simulation_data(file_path: str = SIMULATION_DATA_FILE_PATH) -> pd.DataFrame:
    """Get simulated health insurance data to use for real-world data workflow example"""
    return pd.read_csv(file_path)

def save_simulation_data(df: pd.DataFrame) -> None:
    """Take chunk of test set to use for simulating real-world data workflow example"""
    simulation_data = df.tail(10_000)
    simulation_data.to_csv(SIMULATION_DATA_FILE_PATH,index=False)


def predict_charges(row: dict[str, Any], model: LinearRegression | None = None) -> float:
    if model is None:
        model = load_model()
    X = preprocess(pd.DataFrame(data=[row]))
    X = X.reindex(get_feature_columns(),axis=1).fillna(0).astype(int)
    y_pred = model.predict(X)
    return float(y_pred[0])

if __name__ == "__main__":
    df = get_insurance_data_from_s3()
    save_simulation_data(df)
    df = preprocess(df)
    model = train_model(df)
    save_model(model)
