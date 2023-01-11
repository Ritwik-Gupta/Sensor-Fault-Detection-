from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity import config_entity, artifact_entity
import pandas as pd
import numpy as np
import os,sys
from typing import Optional
from scipy.stats import ks_2samp
from sensor.utils import write_yaml_files
from sensor import config

class DataValidation:
    def __init__(self, 
            data_validation_config: config_entity.DataValidationConfig,
            data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            print(">>"*20 + "DATA VALIDATION STARTS" + "<<"*20)
            self.data_validation_config = data_validation_config
            self.data_ingestion_config = data_ingestion_config
            self.validation_errors = dict()

        except Exception as ex:
            raise SensorException(ex,sys)

    def is_required_colums_exists(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str) -> bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            logging.info("Getting all columns that were removed because of null values > 70 percent.")
            missing_columns = []
            for column in base_columns:
                if column not in current_columns:
                    missing_columns.append(column)

            logging.info(f"Checking if any columns were removed: Missing columns count = {len(missing_columns)}")
            if(len(missing_columns)>0):
                self.validation_errors[report_key_name] = missing_columns
                return False
            
            return True

        except Exception as ex:
            raise SensorException(ex, sys)


    def drop_missing_values_columns(self, df: pd.DataFrame, report_key_name:str) -> Optional[pd.DataFrame]:
        """
        Definition: Drop all the columns that have missing values grater than the threshold
        Parameters:
            df: input dataframe
            threshold: threshold %tage criteria to drop the column
        =====================================================================================
        returns a Pandas Dataframe
        """
        try:
            threshold = self.data_validation_config.missing_threshold
            null_colums = df.columns[df.isna().sum()/df.shape[0] > threshold]

            logging.info(f"Dropping all the null columns if missing values > threshold: Null Columns Count = {len(null_colums)}")

            df.drop(labels=list(null_colums), axis=1, inplace=True)
            if(len(df.columns) == 0):
                logging.info("All columns dropped!")
                return None

            if len(null_colums)>0:
                self.validation_errors[report_key_name] = list(null_colums)
            
            return df
        
        except Exception as ex:
            raise SensorException(ex, sys)

    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str) -> None:
        try:
            self.drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            #we will check if the distribution is same for both datasets(current_df, base_df) for each column
            #if p_value for the distribution is < 0.05 , we do not accept that column/feature

            logging.info("Checking the data drift between the the base dataframe and target dataframe")

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                distribution_check = ks_2samp(base_data, current_data)

                if(distribution_check.pvalue > 0.05):
                    #Accepting the null hypothesis
                    self.drift_report[base_column] = {
                     "p_value" : str(distribution_check.pvalue),
                     "same_distribution" : True
                    }
                else:
                    #Rejecting the null hypothesis
                    self.drift_report[base_column] = {
                     "p_value" : str(distribution_check.pvalue),
                     "same_distribution" : False
                    }
            logging.info(f"Count of columns having same distribution: {len([self.drift_report[x]['same_distribution'] for x in self.drift_report.keys() if self.drift_report[x]['same_distribution']==True])}")
            logging.info(f"Count of columns having different distribution: {len([self.drift_report[x]['same_distribution'] for x in self.drift_report.keys() if self.drift_report[x]['same_distribution']==False])}")


            #adding to validation errors
            self.validation_errors[report_key_name] = self.drift_report

        except Exception as ex:
            raise SensorException(ex, sys)


    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            #getting the original base data as dataframe
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            
            #replacing na values as nan
            base_df.replace(to_replace="na", value=np.nan, inplace=True)
            base_df = self.drop_missing_values_columns(base_df, report_key_name="null_columns_base_data")

            #preparing the train and test df
            train_df = pd.read_csv(self.data_ingestion_config.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_config.test_file_path)

            train_df = self.drop_missing_values_columns(train_df, report_key_name="null_columns_train_data")
            test_df = self.drop_missing_values_columns(test_df, report_key_name="null_columns_test_data")

            #checking if requiered columns exist or not
            column_exist_check_train = self.is_required_colums_exists(base_df, train_df, report_key_name="removed_columns_train")
            column_exist_check_test = self.is_required_colums_exists(base_df, test_df, report_key_name="removed_columns_test")

            #Coverting data types of columns before checking for data drift
            columns_to_exclude = config.TARGET_COLUMN
            base_df = self.convert_datatype_to_float(base_df, columns_to_exclude)
            train_df = self.convert_datatype_to_float(train_df, columns_to_exclude)
            test_df = self.convert_datatype_to_float(test_df, columns_to_exclude)

            #if required cloumns exist is True, we check for data drift
            if column_exist_check_train:
                is_drift_train = self.data_drift(base_df, train_df, report_key_name="data_drift_train")

            if column_exist_check_test:
                is_drift_test = self.data_drift(base_df, test_df, report_key_name="data_drift_test")


            #saving the report in YAML file
            write_yaml_files(file_path=self.data_validation_config.report_file_path, data=self.validation_errors)
            
            data_validation_artifact = artifact_entity.DataValidationArtifact(self.data_validation_config.report_file_path)
            return(data_validation_artifact)

        except Exception as ex:
            raise SensorException(ex, sys)

    def convert_datatype_to_float(self, df: pd.DataFrame, columns_to_exclude:list) -> pd.DataFrame:
        try:
            for column in df.columns:
                if column not in columns_to_exclude:
                    df[column] = df[column].astype("float")

            return df
        
        except Exception as ex:
            raise SensorException(ex, sys)