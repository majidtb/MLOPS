import mlflow

runs = mlflow.search_runs(
    experiment_names=["churn-prediction"],
    order_by=["metrics.f1 DESC"])

colonnes = ["tags.mlflow.runName", "params.n_estimators", "params.max_depth",
            "metrics.accuracy", "metrics.f1"]
print(runs[colonnes].to_string(index=False))

meilleur = runs.iloc[0]
print()
print("Meilleur run :", meilleur["tags.mlflow.runName"], "| id :", meilleur["run_id"][:8], "...")