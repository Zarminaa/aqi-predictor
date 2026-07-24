import pandas as pd
import hopsworks
from dotenv import load_dotenv
import os

# -----------------------------
# Login
# -----------------------------

load_dotenv()

project = hopsworks.login(
        project="project_aqi",
        host="eu-west.cloud.hopsworks.ai",
        port=443,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

fs = project.get_feature_store()

print("Connected to Hopsworks")


# -----------------------------
# Create test data
# -----------------------------

df = pd.DataFrame({
    "datetime": [
        pd.Timestamp("2030-01-01 00:00:00")
    ],
    "value": [
        100.5
    ]
})


print("\nTest dataframe:")
print(df)


# -----------------------------
# Create Hudi feature group
# -----------------------------

fg = fs.get_or_create_feature_group(
    name="hudi_external_test",
    version=1,
    primary_key=["datetime"],
    time_travel_format="HUDI",
    description="Testing Hudi from external Python"
)


print("\nFeature Group:")
print(fg)


# -----------------------------
# Insert first row
# -----------------------------

print("\nInserting first row...")

fg.insert(
    df,
    wait=True
)

print("FIRST INSERT SUCCESS")


# -----------------------------
# Insert more rows
# -----------------------------

df2 = pd.DataFrame({
    "datetime": [
        pd.Timestamp("2030-01-01 01:00:00"),
        pd.Timestamp("2030-01-01 02:00:00"),
        pd.Timestamp("2030-01-01 03:00:00")
    ],
    "value": [
        200.5,
        300.5,
        400.5
    ]
})


print("\nSecond insert:")
print(df2)


fg.insert(
    df2,
    wait=True
)


print("SECOND INSERT SUCCESS")


# -----------------------------
# Read back
# -----------------------------

print("\nFinal data:")

result = fg.read()

print(result)

print("\nShape:")
print(result.shape)