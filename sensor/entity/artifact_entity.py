from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

class DataTransformationArtifact:
    transform_object_path:str
    traformed_train_path:str
    transformed_test_path:str
    target_encoder_path:str

class ModelEvaluationArtifact:...
class ModelPusherArtifact:...
class ModelTrainerArtifact:...