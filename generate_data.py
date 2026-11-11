import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
n = 500

base_dir = Path(__file__).resolve().parent

data = pd.DataFrame({
    "age": np.random.randint(18, 70, n),
    "salaire": np.random.randint(1200, 8000, n),
    "abonnement": np.random.choice(["Basique", "Standard", "Premium"], n),
    "anciennete": np.random.randint(0, 15, n),
    "consommation": np.random.randint(0, 100, n),
})

data["churn"] = (
    (data["consommation"] < 30) &
    (data["anciennete"] < 2)
).astype(int)

output_path = base_dir / "churn_data.csv"
data.to_csv(output_path, index=False)

print(data.head())
print(f"Taux de churn : {data['churn'].mean():.1%}")
print(f"Dataset enregistré dans : {output_path}")
