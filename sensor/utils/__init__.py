from sensor.logger import logging
import pandas as pd
import sys,os
from sensor.config import mongo_client
from sensor.exception import SensorException
import yaml

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

        with open(os.path.basename(file_path), "w") as my_file:
            yaml.dump(data, my_file)

    except Exception as ex:
        raise SensorException(ex, sys)

     