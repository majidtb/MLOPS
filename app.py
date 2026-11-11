from typing import Literal
import mlflow
import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API Churn")

mlflow.set_tracking_uri("sqlite:///mlflow.db")
model = mlflow.sklearn.load_model("models:/churn-model@champion")

class Client(BaseModel):
    age: int
    salaire: float
    abonnement: Literal["Basique", "Standard", "Premium"]
    anciennete: float
    consommation: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(client: Client):
    ligne = pd.DataFrame([client.model_dump()])
    ligne = pd.get_dummies(ligne)
    ligne = ligne.reindex(columns=model.feature_names_in_, fill_value=0)
    resultat = int(model.predict(ligne)[0])
    return {"churn": resultat,
            "message": "Le client va partir" if resultat == 1 else "Le client reste"}