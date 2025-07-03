import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dot, Dense, Activation, BatchNormalization
from tensorflow.keras.optimizers import Adam
from utils.common_functions import read_yaml
from config.paths_config import *
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("Configuration loaded successfully")

        except Exception as e:
            logger.error(f"Error initializing BaseModel: {e}")
            raise CustomException(f"Failed to initialize BaseModel", e)

    def RecommenderNet(self, n_users, n_anime):
        try:
            embedding_size=self.config["model"]["embedding_size"]

            user=Input(name="user", shape=[1])
            #embedding layer for users
            user_embedding=Embedding(name="user_embedding", input_dim=n_users, output_dim=embedding_size)(user)

            anime=Input(name="anime", shape=[1])
            #embedding layer for anime
            anime_embedding=Embedding(name="anime_embedding", input_dim=n_anime, output_dim=embedding_size)(anime)

            #calculating dot product i.e similiarity between user and anime
            x=Dot(name="dot_product", normalize=True, axes=2)([user_embedding, anime_embedding])

            #flattening the output
            x=Flatten()(x)

            #denser layer
            x=Dense(1, kernel_initializer="he_normal")(x)

            #batch normalization layer
            x=BatchNormalization()(x)

            #activation layer
            x=Activation("sigmoid")(x)

            model=Model(inputs=[user, anime], outputs=x)
            model.compile(
                loss=self.config["model"]["loss"],
                optimizer=self.config["model"]["optimizer"],
                metrics=self.config["model"]["metrics"]
            )            
            logger.info("RecommenderNet model created successfully")
            return model
        
        except Exception as e:
            logger.error(f"Error in RecommenderNet: {e}")
            raise CustomException(f"Failed to create RecommenderNet", e)
