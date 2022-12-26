from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self, data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self) -> artifact_entity.DataIngestionArtifact:
        try:
            logging.info("Exporting data from mongodb collection to pandas dataframe")
            #Exporting all data from mongodb into pandas dataframe
            df: pd.DataFrame = utils.get_collection_as_dataframe(
                self.data_ingestion_config.database_name, 
                self.data_ingestion_config.collection_name)

            #replacing na values with np.Nan if any present
            df.replace(to_replace="na", value=np.nan, inplace=True)

            logging.info("Storing entire data into feature store directory")
            #ceating feature store directory 
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(name=feature_store_dir, exist_ok=True)

            #saving df to feature store directory
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index=False)

            logging.info("Splitting data into train and test and storing in datasets folder")
            #splitting data into train and test files
            #creating train test file path
            train_test_filepath = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(name=train_test_filepath, exist_ok=True)
            train_data, test_data = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=42)
            train_data.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, index=False)
            test_data.to_csv(path_or_buf=self.data_ingestion_config.test_file_path, index=False)

            #Prepare the artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                self.data_ingestion_config.feature_store_file_path,
                self.data_ingestion_config.train_file_path,
                self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as ex:
            raise SensorException(ex, sys)