import pandas as pd

df = pd.read_csv("A:/Dissertation/MediMate/MediMate/Datasets/filtered_drug_interactions.csv")

df["text"] = df.apply(
    lambda row: f"{row['Drug_A']} + "
                f"{row['Drug_B']}",
    axis=1
)
df = df.rename(columns={"Level": "label"})


df = df[["text", "label"]]

df.to_csv("A:/Dissertation/MediMate/MediMate/Datasets/filtered_drug_interactions.csv", index=False)
print("Finished")