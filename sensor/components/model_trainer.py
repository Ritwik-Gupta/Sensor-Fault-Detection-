from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException
import os,sys
import xgboost as xgb
from sensor import utils
from sklearn.metrics import f1_score


class ModelTrainer:
    def __init__(self, 
            model_trainer_config:config_entity.ModelTrainerConfig,
            data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            pass
        
        except Exception as ex:
            raise SensorException(ex, sys)

    def train_model(self,x,y):
        try:
            xgb_clf = xgb.XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as ex:
            raise SensorException(ex, sys)


    def initiate_model_trainer(self):
        try:
            logging.info("======Model Training Starts======")
            logging.info("Loading test and train numpy array after transformation")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info("Splitting train and test data into X and y data")
            x_train,y_train = train_arr[:,:-1], train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1], test_arr[:,-1]

            logging.info("Training the model")
            model = train_model(x_train, y_train)
            y_hat_train = model.predict(x_train)
            y_hat_test = model.predict(x_test)

            logging.info("Getting the accuracy scores")
            f1score_train = f1_score(y_hat_train,y_train)
            f1score_test= f1_score(y_hat_test,y_test)

            logging.info(f"f1 train score: {f1score_train} || f1 test score: {f1score_test}")

            logging.info("Checking for underfitting and overfitting of the data")
            #check for accuracy on testing data (underfitting)
            if(f1score_test < self.model_trainer_config.expected_score):
                raise Exception(f"Accuracy score:{f1score_test} || Model is not good -> Accuracy is low || \
                                Expected Accuracy score: {self.model_trainer_config.expected_score}")
            
            #checking for overfitting
            diff = abs(f1score_test-f1score_train)

            if diff < self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Difference b/w training and testing score is high || difference = {diff} \
                                Expected diference should be less than {self.model_trainer_config.overfitting_threshold}")

            logging.info("Saving the model in model training directory")
            #save the trained model
            utils.save_object(file_path=self.model_trainer_config.model_path, model=model)

            logging.info("Preparing and returning the model training artifact")
            #preparing the Model Training artifact
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path = self.model_trainer_config.model_path,
                f1_train_score = f1score_train,
                f1_test_score = f1score_test
            )
            logging.info("======Model Training Ends======")

            return model_trainer_artifact

        except Exception as ex:
            raise SensorException(ex, sys)