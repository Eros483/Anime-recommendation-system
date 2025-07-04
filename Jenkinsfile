pipeline {
    agent any

    environment  {
        VENV_DIR = 'venv'
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
    }
}