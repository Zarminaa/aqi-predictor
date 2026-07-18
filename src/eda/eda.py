import pandas as pd

from analyzer import EDAAnalyzer


df = pd.read_csv("data/processed/lahore_merged.csv")

df["datetime"] = pd.to_datetime(df["datetime"])


eda = EDAAnalyzer(df)

eda.run()