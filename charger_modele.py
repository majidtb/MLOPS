import mlflow
import mlflow.sklearn
import pandas as pd

runs = mlflow.search_runs(experiment_names=["churn-prediction"],
                          order_by=["metrics.f1 DESC"])
run_id = runs.iloc[0]["run_id"]

model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
print("Modele recharge :", type(model).__name__)
print("Nombre de variables attendues :", model.n_features_in_)

client = pd.DataFrame([{
    "age": 35, "salaire": 2500, "anciennete": 1, "consommation": 10,
    "abonnement_Premium": False, "abonnement_Standard": True,
}])

client = client[list(model.feature_names_in_)]

print("Le client va-t-il partir ? ->", "OUI" if model.predict(client)[0] == 1 else "NON")