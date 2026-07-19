import joblib


def predict(model_path, X):
    """
    Load a model and make predictions.
    """

    model = joblib.load(model_path)

    predictions = model.predict(X)

    return predictions