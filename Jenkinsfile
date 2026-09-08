pipeline {
    agent any

    environment {
        IMAGE_NAME = 'api-notas'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                    pytest -v
                '''
            }
        }

        stage('Build imagen') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG -t $IMAGE_NAME:latest .'
            }
        }
    }

    post {
        success { echo "Imagen construida: ${IMAGE_NAME}:${IMAGE_TAG}" }
        failure { echo 'El pipeline falló' }
    }
}