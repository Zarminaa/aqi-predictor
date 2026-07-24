from src.hopsworks.client import get_project


def get_model_registry():

    project = get_project()

    return project.get_model_registry()