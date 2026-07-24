from src.hopsworks.client import get_project

FEATURE_VIEW_NAME = "aqi_training_view"
FEATURE_VIEW_VERSION = 1

TARGET_COLUMNS = [
    "target_day1",
    "target_day2",
    "target_day3",
]


def get_feature_view():
    """
    Get the AQI Feature View.
    Creates it if it does not already exist.
    """

    project = get_project()
    fs = project.get_feature_store()

    fv = fs.get_feature_view(
        name=FEATURE_VIEW_NAME,
        version=FEATURE_VIEW_VERSION,
    )

    if fv is None:

        print("Creating Feature View...")

        fg = fs.get_feature_group(
            name="aqi_features_hudi",
            version=1,
        )

        query = fg.select_all()

        fv = fs.create_feature_view(
            name=FEATURE_VIEW_NAME,
            version=FEATURE_VIEW_VERSION,
            query=query,
            labels=TARGET_COLUMNS,
            description="AQI 3-Day Forecasting Feature View",
        )

        print("Feature View created.")

    else:

        print("Using existing Feature View.")

    return fv