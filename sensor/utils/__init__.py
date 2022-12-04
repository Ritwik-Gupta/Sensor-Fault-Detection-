from sensor.logger import logging
import pandas as pd
import sys
from sensor.config import mongo_client
from sensor.exception import SensorException

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
            df.drop(["_id"],axis=1,inplace=True)
            
        return df    
        
    except Exception as e:
        raise SensorException(e, sys)