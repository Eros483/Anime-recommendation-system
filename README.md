# Hybrid Anime Recommendation System
## Overview
This system serves as a combination of a user-based recommendation system, wherein a user is provided recommendations, based on content consumed by similiar users, and a content-based recommendation system, wherein recommendations are draw from media similiar to anime already viewed by the user.

The entire pipeline had been deployed using Jenkins for the CI/CD pipeline, and Google Kubernetes Engine as the deployed platform for the dockerized algorithm, hosted on google cloud registry.
Utilised comet-ml for model experiment tracking.

## Installation for local usage
### 1. Clone the repository:
```
git clone https://github.com/Eros483/Anime-recommendation-system.git
cd Anime-recommendation-system
```
### 2. Environment set up
We recommend using anaconda for environment management.
```
conda env create -f environment.yml
conda activate anime
```
Alternatively create a `venv` and run `pip install -e .` using the provided `setup.py`.
### 3. Launch the system
```
python application.py
```

## Directory Structure
```
Anime-recommendation-system
│   .dvcignore
│   .gitignore
│   application.py
│   deployment.yaml
│   Dockerfile
│   environment.yml
│   Jenkinsfile
│   README.md
│   requirements.txt
│   setup.py
│
├───artifacts
│   │   .gitignore
│   │   model.dvc
│   │   model_checkpoint.dvc
│   │   processed.dvc
│   │   raw.dvc
│   │   weights.dvc
│   │
│   ├───model
│   │       model.h5
│   │
│   ├───model_checkpoint
│   │       weights.weights.h5
│   │
│   ├───processed
│   │       anime2anime_decoded.pkl
│   │       anime2anime_encoded.pkl
│   │       df.csv
│   │       rating_df.csv
│   │       synopsis_df.csv
│   │       user2user_decoded.pkl
│   │       user2user_encoded.pkl
│   │       X_test_array.pkl
│   │       X_train_array.pkl
│   │       y_test.pkl
│   │       y_train.pkl
│   │
│   ├───raw
│   │       anime.csv
│   │       animelist.csv
│   │       anime_with_synopsis.csv
│   │
│   └───weights
│           anime_weights.pkl
│           user_weights.pkl
│
├───config
│   │   config.yaml
│   │   paths_config.py
│   │   __init__.py
│
├───custom_jenkins
│       Dockerfile
│
├───notebook
│       anime.ipynb
│
├───pipeline
│   │   prediction_pipeline.py
│   │   training_pipeline.py
│   │   __init__.py
│
├───src
│   │   base_model.py
│   │   custom_exception.py
│   │   data_ingestion.py
│   │   data_processing.py
│   │   logger.py
│   │   model_training.py
│   │   __init__.py
│
├───static
│       style.css
│
├───templates
│       index.html
│
└───utils
    │   common_functions.py
    │   helpers.py
    │   __init__.py
```
## Application working explaination
### Dataset utilisation
1. The dataset was retrieved from [Kaggle](https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020).
2. we utilised `dvc` for data versioning, and stored the relevant files on `google cloud buckets`.
### Data Processing
1. First we removed infrequent users, setting a minimum of 400 reviews.
2. We scaled ratings to a range of 0-1, to prevent the model from creating irrelevant patterns between on sequential numeric values.
3. We extracted unique users, and unique animes, then encoded them, once again to prevent creation of irrelevant patterns.
4. Shuffled data to ensure even distribution. 
5. Replaced unknown values with `nan`.
 
### Model Architecture
- Utilised a Neural Collaborative Filtering model.
- Allowed inputs as single User IDs and single anime IDs.
- Embedded animes to create vectors.
- Computed cosine similarity.
- Used sigmoid function to squash values into a 0-1 range.
- Chose `MAE` and `MSE` for metrics, and `binary_crossentropy` for loss.
- Extracted weights for future usage.

### Content based recommendation system creation
1. Looks up anime ID by referencing anime weights.
2. Computes `dot product` between all anime weights and the provided anime id.
3. Sorts values, and returns top `n` animes.

### User based recommendation system creation
1. Works the same as content based system idea, but uses user ID and user weights instead, to get top-n similiar users.
2. Finds the top 25% anime genres preferred by user.
3. Gets user recommendations by combining similiar users, and preferred genres.

### Hybrid Recommendation system
Adds weight to suggestions provided by content and user based recommendation systems, and returns the total top `n` highest scored animes.

### API creation
Created using flask endpoints.

### UI creation
HTML + CSS styling.
