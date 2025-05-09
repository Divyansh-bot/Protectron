import pandas as pd

# ✅ Replace this with the path to your dataset
dataset_path = "data/datasets/app_permission_dataset.csv"

try:
    df = pd.read_csv(dataset_path)
    print("✅ Column Names:")
    for col in df.columns:
        print(f"- {col}")
except Exception as e:
    print("❌ Error loading file:", e)
