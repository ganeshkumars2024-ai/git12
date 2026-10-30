
pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select the Wishlist version to build'
        )
    }

    environment {
        IMAGE_NAME = '24mis0260/wishlist'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build --build-arg APP_VERSION=%VERSION% -t %IMAGE_NAME%:%VERSION% .'
            }
        }

        stage('Docker Hub Login and Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        powershell -NoProfile -Command "$env:DOCKERHUB_TOKEN | docker login -u $env:DOCKERHUB_USER --password-stdin"
                        docker push %IMAGE_NAME%:%VERSION%
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Wishlist Docker image built and pushed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
