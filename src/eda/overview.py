def dataset_overview(df):

    print("\nDATASET INFO")
    print(df.info())

    print("\nHEAD")
    print(df.head())

    print("\nSUMMARY")
    print(df.describe())

    print("\nMISSING VALUES")
    print(df.isnull().sum())

    print("\nDUPLICATES")
    print(df.duplicated().sum())