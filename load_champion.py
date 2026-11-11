import mlflow
import mlflow.sklearn
import pandas as pd

mlflow.set_tracking_uri("sqlite:///mlflow.db")

model = mlflow.sklearn.load_model("models:/churn-model@champion")
print("Modele charge :", type(model).__name__)
print("Variables attendues :", list(model.feature_names_in_))

client = pd.DataFrame([{
    "age": 35, "salaire": 2500, "anciennete": 1, "consommation": 10,
    "abonnement_Premium": False, "abonnement_Standard": True,
}])
client = client[list(model.feature_names_in_)]

print("Le client va-t-il partir ? ->", "OUI" if model.predict(client)[0] == 1 else "NON")