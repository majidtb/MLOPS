import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri("sqlite:///mlflow.db")

runs = mlflow.search_runs(
    experiment_names=["churn-prediction"],
    order_by=["metrics.f1 DESC"])
best = runs.iloc[0]
run_id = best["run_id"]
print("Meilleur run :", best["tags.mlflow.runName"], "| id :", run_id[:8], "...")

result = mlflow.register_model(f"runs:/{run_id}/model", "churn-model")
print("Modele enregistre : churn-model | version", result.version)

client = MlflowClient()
client.set_registered_model_alias("churn-model", "champion", result.version)
print("Alias 'champion' -> version", result.version)