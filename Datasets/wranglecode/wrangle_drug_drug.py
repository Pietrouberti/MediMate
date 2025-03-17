import pandas as pd

df = pd.read_csv("A:/Dissertation/MediMate/MediMate/Datasets/filtered_drug_interactions.csv")

df["text"] = df.apply(
    lambda row: f"DDI ID A: {row['DDInterID_A']} / Drug A: {row['Drug_A']} | "
                f"DDI ID B: {row['DDInterID_B']} / Drug B: {row['Drug_B']}",
    axis=1
)
df = df.rename(columns={"Level": "label"})


df = df[["text", "label"]]

df.to_csv("A:/Dissertation/MediMate/MediMate/Datasets/filtered_drug_interactions.csv", index=False)
print("Finished")