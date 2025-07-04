pipeline {
    agent any

    environment  {
        VENV_DIR = 'venv'
        GCP_PROJECT='top-virtue-464214-m6'
        GCLOUD_PATH='var/jenkins_home/google-cloud-sdk/bin'
        KUBECTL_AUTH_PLUGIN='/usr/lib/google-cloud-sdk/bin'
    }

    stages{
        stage("Cloning from github..."){
            steps{
                script{
                    echo 'Cloning from github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Eros483/Anime-recommendation-system.git']])
                }
            }
        }

        stage("Making a virtual evnironment"){
            steps{
                script{
                    echo 'making a venv'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }

        stage("DVC PULL"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key-anime', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'DVC PULL'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
        stage("Build and push image to GCR"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key-anime', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'pushing image to gcr'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }

        stage("Deploying to kubernetes"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key-anime', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'deploying to kubernetes'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-app-cluster --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}