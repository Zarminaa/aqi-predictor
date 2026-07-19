from src.data.load_data import load_features
from src.data.split_data import split_data


# Load dataset
df = load_features()

print("Dataset loaded")
print(df.head())
print(df.shape)


# Split dataset
(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test,
) = split_data(
    df,
    target="target_day1"
)


print("\nSplit complete")

print("X_train:", X_train.shape)
print("X_val:", X_val.shape)
print("X_test:", X_test.shape)

print("\ny_train:", y_train.shape)
print("y_val:", y_val.shape)
print("y_test:", y_test.shape)