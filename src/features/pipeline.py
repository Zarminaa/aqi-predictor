from src.features.time_features import add_time_features
from src.features.cyclical_features import add_cyclical_features
from src.features.lag_features import add_lag_features
from src.features.rolling_features import add_rolling_features
from src.features.trend_features import add_trend_features
from src.features.interaction_features import add_interaction_features
from src.features.target_features import add_targets


def engineer_features(df, add_target_features=True):

    df = add_time_features(df)
    df = add_cyclical_features(df)
    df = add_lag_features(df)
    df = add_rolling_features(df)
    df = add_trend_features(df)
    df = add_interaction_features(df)

    if add_target_features:
        df = add_targets(df)

    df.drop(
        columns=[
            "hour",
            "month",
            "day_of_week",
            "wind_direction_10m",
        ],
        inplace=True,
    )

    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df