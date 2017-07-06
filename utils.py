import pickle
import yaml
import os

def load_parameters(root):
    with open(os.path.join(root,"parameters.yml"), "r") as ymlfile:
        return yaml.load(ymlfile)

def pickle_data(data, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(data, file)

def load_pickle(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)