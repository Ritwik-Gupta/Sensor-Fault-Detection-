import os
import pandas as pd
import pymongo
import json
from dataclasses import dataclass

@dataclass
class EnvironmentVariable:
    mongodb_url:str = os.getenv("MONGODB_URI")
    aws_access_key:str = os.getenv("AWS_ACCESS_KEY")
    aws_secret_key:str = os.getenv("AWS_SECRET_KEY")


env_vars = EnvironmentVariable()

#create mongo connection
mongo_client = pymongo.MongoClient(env_vars.mongodb_url)

