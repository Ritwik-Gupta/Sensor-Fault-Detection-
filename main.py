from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import get_collection_as_dataframe
from sensor.entity import config_entity,artifact_entity
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
import sys


if __name__=="__main__":
     try:
          #Training Pipeline
          logging.info("Initiating Training Pipeline")
          training_pipeline_config = config_entity.TrainingPiplelineConfig()

          #Data Ingestion 
          logging.info("Initiating Data Ingestion")
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config = training_pipeline_config)
          data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
          logging.info("Data Ingestion completed")

          #Data Validation
          logging.info("Initiating Data Validation")
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config, 
                              data_ingestion_config=data_ingestion_config)
          data_validation_artifact = data_validation.initiate_data_validation()
          logging.info("Data Validation Completed")

          #Data Transformation
          logging.info("Initiating Data Transformation")
          data_tranformation_config = config_entity.DataTransformationConfig(training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_tranformation_config, 
                                   data_ingestion_artifact= data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()
          logging.info("Data Transformation Completed")

          #Model Training
          logging.info("Initiating Model Training")
          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config)
          model_trainer = ModelTrainer(model_trainer_config = model_trainer_config, 
                              data_transformation_artifact = data_transformation_artifact)
          model_trainer_artifact = model_trainer.initiate_model_training()
          logging.info("Model Training Completed")




     except Exception as ex:
          raise SensorException(ex, sys)
