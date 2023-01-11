from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
from sklearn.preprocessing import Pipeline
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler 
from sklearn.preprocessing import LabelEncoder
from sensor.config import TARGET_COLUMN
from sensor import utils
import os,sys

class DataTransformation:
    def __init__(self, data_transformation_config: config_entity.DataTransformationConfig,
                    data_transformation_artifact: artifact_entity.DataTransformationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)
    
    @classmethod
    def get_transformer_object(cls) -> Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            robust_scaler = RobustScaler()

            pipeline = Pipeline(steps=[
                    ('Imputer', simple_imputer),
                    ('RobustScaler', robust_scaler)
                ])
            return pipeline
        
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self) -> artifact_entity.DataTransformationArtifact:
        try:
            #reading training and testing files
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df = train_df.drop(labels=[TARGET_COLUMN], axis=1)
            input_feature_test_df = test_df.drop(labels=[TARGET_COLUMN], axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_test_df)

            #transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            #transforming input features
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            smt = SMOTETomek(sampling_strategy="minority")

            print("Shape of training dataset before sampling: {} , testing dataset: {}".format(input_feature_train_arr.shape, input_feature_test_arr.shape))
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            input_feature_test_arr ,target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            print("Shape of training dataset After sampling: {} , testing dataset: {}".format(input_feature_train_arr.shape, input_feature_test_arr.shape))

            #concate training and testing numpy arrays into single 2d arrays
            training_array = np._c(input_feature_train_arr, target_feature_train_arr)
            testing_array = np.c_(input_feature_test_arr, target_feature_test_arr)

            #saving the training and testing numpy array as numpy object files
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_train_path,
                                        np_array = training_array)
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_test_path, 
                                        np_array = testing_array)

            #saving the transformation models and encoder models as pkl files
            utils.save_object(file_path = self.data_transformation_config.transform_object_path, 
                              obj = transformation_pipeline)

            utils.save_object(file_path = self.data_transformation_config.target_encoder_path, 
                              obj = label_encoder)

            
            #Preparing the data transformation artifact
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path = self.data_transformation_artifact.transform_object_path,
                traformed_train_path = self.data_transformation_artifact.transformed_train_path,
                transformed_test_path = self.data_transformation_artifact.transformed_test_path,
                target_encoder_path = self.data_transformation_artifact.target_encoder_path
            )

            logging.info(f"Data Transformation object {data_transformation_artifact}")
            logging.info("Data Transformation Completed!")

            return data_transformation_artifact

        except Exception as ex:
            raise SensorException(ex, sys)