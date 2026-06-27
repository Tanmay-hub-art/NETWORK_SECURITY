import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.entity.artifact_intity import DataTransformationArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException 
from network_security.logging.logger import logging 
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object



class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config :DataTransformationConfig ):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def get_data_trainsformer_object(cls)->Pipeline:
        logging.info('Entered get_data_trainsformer_object method of transformer class ')
        try:
            imputer:KNNImputer =  KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f'Initialize KNN imputer with params { DATA_TRANSFORMATION_IMPUTER_PARAMS }')

            processor:Pipeline = Pipeline(
                [
                    ('imputer',imputer)
                ]
            )

            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info('Entered the data transforamtion method of data transformation class')
        try:
            logging.info('starting the data transformation')
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_path)

            ##training data frame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)


            ##Testing data frame
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor_object = self.get_data_trainsformer_object()
            transformed_input_feature_train = preprocessor_object.fit_transform(input_feature_train_df)
            transformed_input_feature_test = preprocessor_object.fit_transform(input_feature_test_df)

            train_arry = np.c_[ transformed_input_feature_train,np.array(target_feature_train_df)  ]
            test_arry = np.c_[ transformed_input_feature_test,np.array(target_feature_test_df)  ]


            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arry)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arry )
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)


            save_object("final_model/preprocessor.pkl",preprocessor_object)


            data_transformation_artifact= DataTransformationArtifact(
                transformed_object_file_path  = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
                )
            

            return data_transformation_artifact
            

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        