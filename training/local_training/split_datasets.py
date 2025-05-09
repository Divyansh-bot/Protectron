import pandas as pd
from sklearn.model_selection import train_test_split

dataset_path = "data/datasets/"

# Split function
def split_dataset(file_name, test_size=0.2):
    df = pd.read_csv(dataset_path + file_name)
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)

    train_df.to_csv(dataset_path + "train_" + file_name, index=False)
    test_df.to_csv(dataset_path + "test_" + file_name, index=False)

    print(f"✅ Split {file_name}: Train ({len(train_df)}) | Test ({len(test_df)})")

# Split each dataset
split_dataset("user_behavior.csv")
split_dataset("network_intrusion.csv")
split_dataset("file_access.csv")
split_dataset("reverse_shell.csv")
