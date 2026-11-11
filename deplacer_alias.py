import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri("sqlite:///mlflow.db")
client = MlflowClient()

runs = mlflow.search_runs(experiment_names=["churn-prediction"],
                          filter_string="tags.mlflow.runName = 'essai-2'")
run_id = runs.iloc[0]["run_id"]

v = mlflow.register_model(f"runs:/{run_id}/model", "churn-model")
print("Nouvelle version creee :", v.version)

actuel = client.get_model_version_by_alias("churn-model", "champion")
print("Champion actuel : version", actuel.version)

client.set_registered_model_alias("churn-model", "champion", v.version)
print("Apres deplacement : champion -> version",
      client.get_model_version_by_alias("churn-model", "champion").version)
client.set_registered_model_alias("churn-model", "champion", actuel.version)
print("Apres retour : champion -> version",
      client.get_model_version_by_alias("churn-model", "champion").version)