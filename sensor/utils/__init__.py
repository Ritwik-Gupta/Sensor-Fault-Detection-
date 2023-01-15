from sensor.logger import logging
import pandas as pd
import numpy as np
import sys,os
from sensor.config import mongo_client
from sensor.exception import SensorException
import yaml
import dill

def get_collection_as_dataframe(database_name:str,collection_name:str) -> pd.DataFrame:
    """
    Description: This function returns collection as a DataFrame
    Params:
        database_name: Database Name
        collection_name: Collection Name
    =============================================
    return Pandas DataFrame of a collection
    """
    try:
        logging.info("Connecting to mongo and retrieving data")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))

        if("_id" in df.columns):
            df.drop(labels = ["_id"],axis=1,inplace=True)
            
        return df    
        
    except Exception as e:
        raise SensorException(e, sys)


def write_yaml_files(file_path, data:dict):
    try:
        file_dirname = os.path.dirname(file_path)
        os.makedirs(file_dirname, exist_ok=True)

        with open(file_path, "w") as my_file:
            yaml.dump(data, my_file)

    except Exception as ex:
        raise SensorException(ex, sys)

def save_object(file_path:str, obj:object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        logging.info("Dumping pickle file into folder")
        with open(file_path, "wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info("dumping completed")
    except Exception as ex:
        raise SensorException(ex, sys)

def load_object(file_path:str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The specified file {file_path} does not exist!")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as ex:
        raise SensorException(ex, sys)

def save_numpy_array_data(file_path:str, np_array:np.arr):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, np_array)
    except Exception as ex:
        raise SensorException(ex, sys)

def load_numpy_array_data(file_path:str) -> np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The specified file path {file_path} does not exist!!")
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as ex:
        raise SensorException(ex, sys)