from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import get_collection_as_dataframe
import sys

def test_logger():
     try:
          logging.info("Logging Start")
          return 3/0
     except Exception as e:
          raise SensorException(error_message=e, error_detail=sys)


if __name__=="__main__":
     try:
          logging.info("calling get_collection_as_dataframe function")
          my_df = get_collection_as_dataframe(database_name="SensorDB", collection_name="SensorData")
          print(my_df.head())
     except Exception as e:
          print(e)
