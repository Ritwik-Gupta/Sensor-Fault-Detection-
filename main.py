from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import get_collection_as_dataframe
from sensor.entity import config_entity 
from sensor.components import data_ingestion,data_validation
import sys


if __name__=="__main__":
     try:
          #Training Pipeline
          logging.info("Initiating Training Pipeline")
          training_pipeline_config = config_entity.TrainingPiplelineConfig()

          #Data Ingestion 
          logging.info("Initiating Data Ingestion")
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
          data_ingestion = data_ingestion.DataIngestion(data_ingestion_config = data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
          logging.info("Data Ingestion completed")

          #Data Validation
          logging.info("Initiating Data Validation")
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config)
          data_validation = data_validation.DataValidation(data_validation_config=data_validation_config, 
                              data_ingestion_config=data_ingestion_config)
          data_validation_artifact = data_validation.initiate_data_validation()
          logging.info("Data Validation Completed")

     except Exception as ex:
          raise SensorException(ex, sys)
