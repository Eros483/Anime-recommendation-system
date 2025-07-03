import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger=get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config['bucket_name']
        self.file_names = self.config['bucket_file_names']
        
        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Initialized Data Ingestion with bucket: {self.bucket_name} and files: {self.file_names}")

    def download_csv_from_gcp(self):
        try:
            logger.info("Starting download of CSV files from GCS")
            
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            if not os.path.exists(RAW_DIR):
                os.makedirs(RAW_DIR)

            for file_name in self.file_names:
                file_path=os.path.join(RAW_DIR, file_name)
                if file_name=="animelist.csv":
                    blob=bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    data=pd.read_csv(file_path, nrows=5000000)
                    data.to_csv(file_path, index=False)
                    logger.info(f"Downloaded and saved only 5m rows")
                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)
                    logger.info(f"Downloaded {file_name} to {file_path}")
            logger.info("All files downloaded successfully from GCS")

        except Exception as e:
            logger.error("Error in downloading data from GCS")
            raise CustomException("Failed to download data from GCS", e)
        
    def run(self):
        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            logger.info("Data ingestion process completed successfully")
        except Exception as e:
            logger.error("Error in data ingestion process")
            raise CustomException("Data ingestion failed", e)
        finally:
            logger.info("Data ingestion process finished")

if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()