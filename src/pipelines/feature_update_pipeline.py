import pandas as pd

from src.features.pipeline import engineer_features
from src.supabase.supabase_client import supabase
from src.supabase.hopsworks_client import get_feature_group



def get_last_processed():

    response = (
        supabase.table("pipeline_state")
        .select("last_processed")
        .eq("pipeline_name", "feature_pipeline")
        .single()
        .execute()
    )

    return response.data["last_processed"]




def update_last_processed(timestamp):

    supabase.table("pipeline_state").update(
        {
            "last_processed": timestamp
        }
    ).eq(
        "pipeline_name",
        "feature_pipeline"
    ).execute()





def load_merged():

    all_rows = []

    start = 0


    while True:

        response = (
            supabase.table("merged")
            .select("*")
            .order("datetime")
            .range(start, start + 999)
            .execute()
        )


        if not response.data:
            break


        all_rows.extend(
            response.data
        )

        start += 1000



    df = pd.DataFrame(all_rows)


    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )


    return df







def fix_feature_dtypes(df):

    """
    Force dataframe types to match Hopsworks Feature Group schema
    """

    df = df.copy()



    # -----------------------------
    # datetime
    # -----------------------------

    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )




    # -----------------------------
    # Hopsworks BIGINT columns
    # -----------------------------

    bigint_columns = [

        "us_aqi",

        "relative_humidity_2m",

        "cloud_cover",

        "day",

        "day_of_year",

        "is_weekend"

    ]



    for col in bigint_columns:

        if col in df.columns:

            df[col] = (

                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

                .fillna(0)

                .round()

                .astype("int64")

            )





    # -----------------------------
    # Hopsworks DOUBLE columns
    # -----------------------------

    for col in df.columns:


        if (

            col != "datetime"

            and col not in bigint_columns

        ):


            df[col] = (

                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

                .astype("float64")

            )



    return df








def main():


    # -----------------------------
    # 1. Get checkpoint
    # -----------------------------

    last_processed = get_last_processed()


    print(
        "Last processed:",
        last_processed
    )





    # -----------------------------
    # 2. Load merged data
    # -----------------------------

    merged = load_merged()


    print(
        "Merged shape:",
        merged.shape
    )





    # -----------------------------
    # 3. Feature engineering
    # -----------------------------

    features = engineer_features(

        merged,

        add_target_features=True

    )


    features["datetime"] = pd.to_datetime(
        features["datetime"]
    )





    # -----------------------------
    # 4. Select only new features
    # -----------------------------

    new_features = features[

        features["datetime"]

        >

        pd.to_datetime(last_processed)

    ].copy()



    print(
        "All features shape:",
        features.shape
    )


    print(
        "New features shape:",
        new_features.shape
    )





    if new_features.empty:


        print(
            "No new features to insert"
        )

        return






    # -----------------------------
    # 5. Fix types
    # -----------------------------

    new_features = fix_feature_dtypes(
        new_features
    )





    print(
        "\nFINAL TYPES BEFORE HOPSWORKS\n"
    )


    for col in new_features.columns:

        print(
            col,
            "---->",
            new_features[col].dtype
        )






    # -----------------------------
    # 6. Get feature group
    # -----------------------------

    fg = get_feature_group()
    print("Feature Group:", fg.name)
    print("Version:", fg.version)
    print("Primary key:", fg.primary_key)


    print(
        "\nChecking Feature Group schema...\n"
    )


    for feature in fg.schema:

        print(
            feature.name,
            "---->",
            feature.type
        )

    # -----------------------------
    # 7. Insert
    # -----------------------------

    print(
        "\nInserting into Hopsworks..."
    )



    fg.insert(

        new_features,

        write_options={

            "wait_for_job": True

        }

    )



    print(
        f"\nInserted {len(new_features)} rows into Hopsworks"
    )






    # -----------------------------
    # 8. Update checkpoint
    # -----------------------------

    latest_timestamp = (

        new_features["datetime"]

        .max()

        .strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

    )



    update_last_processed(
        latest_timestamp
    )



    print(
        "Pipeline state updated:",
        latest_timestamp
    )


if __name__ == "__main__":

    main()