import logging
import os
from datetime import datetime
import os

#log file name
log_file_name = f"{datetime.now().strftime('%m%d%Y %H%M%S')}.log"

#log file path
log_file_path = os.path.join(os.getcwd(),"Logs")

if not os.path.exists(log_file_path):
   os.makedirs(log_file_path)

   logging.basicConfig(
    filename = os.path.join(log_file_path,log_file_name),
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
   )

