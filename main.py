from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from network_security.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == '__main__':
    try:
        training_pipeline_conifg = TrainingPipelineConfig()
        data_ingestion_conifg = DataIngestionConfig(training_pipeline_conifg)
        data_ingestion = DataIngestion(data_ingestion_conifg)
        logging.info('Initiate data ingestion')
        dataingestionartifact=data_ingestion.initiate_date_ingestion()
        print(dataingestionartifact) 
        logging.info('Data initation completed')
        data_validation_conifg = DataValidationConfig(training_pipeline_conifg)
        data_validation = DataValidation(dataingestionartifact,data_validation_conifg)
        logging.info('Initiate the data validation ')
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info('Data validation completed')
        print(data_validation)
        data_transformation_config = DataTransformationConfig(training_pipeline_conifg)
        logging.info('Data Transformation started!')
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation() 
        print(data_transformation_artifact)
        logging.info('Data Transformation completed!')

        logging.info("Model Training sstared")
        model_trainer_config=ModelTrainerConfig(training_pipeline_conifg)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()


        
        
    except Exception as e:
        print(e)
        logging.info('Divide by zero error')
        raise NetworkSecurityException(e,sys)