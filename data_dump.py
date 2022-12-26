import pymongo
import pandas as pd
import json

client = pymongo.MongoClient("mongodb+srv://ritwik97:Arc%407245@cluster1.tkkbuh8.mongodb.net/?retryWrites=true&w=majority")

# Database Name
dataBase = client["SensorDB"]

# Collection  Name
collection = dataBase['SensorData']

#Data file path
file_path = "aps_failure_training_set1.csv"


if __name__ == "__main__":
    try :
        data = pd.read_csv(file_path)
        print(data.shape)
        data.reset_index(inplace=True, drop=True)

        json_records = list(json.loads(data.T.to_json()).values())

        print(json_records[0])
        collection.insert_many(json_records)

    except Exception as e:
        print(e)