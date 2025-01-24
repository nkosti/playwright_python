import json
import logging
import os


def load_env_data(env_name):
    path = os.path.dirname(__file__)
    try:
        with open(f"{path}/environments/{env_name.lower()}.json") as dataset:
            dataset_loaded = json.loads(dataset.read())
        return dataset_loaded
    except FileNotFoundError as e:
        logging.error(f"Error while reading config file. {e}")
