
pipeline {
    agent any

    environment {
        IMAGE_NAME = '24mis0260/wishlist'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Wishlist source code checked out'
            }
        }

        stage('Build V1 - Add') {
            steps {
                bat 'docker build --build-arg APP_VERSION=v1 -t 24mis0260/wishlist:v1 .'
            }
        }

        stage('Build V2 - Remove') {
            steps {
                bat 'docker build --build-arg APP_VERSION=v2 -t 24mis0260/wishlist:v2 .'
            }
        }

        stage('Build V3 - View') {
            steps {
                bat 'docker build --build-arg APP_VERSION=v3 -t 24mis0260/wishlist:v3 .'
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    bat '''
                        echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                    '''
                }
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                bat '''
                    docker push 24mis0260/wishlist:v1
                    docker push 24mis0260/wishlist:v2
                    docker push 24mis0260/wishlist:v3
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: All three Wishlist images pushed to Docker Hub!'
        }
        failure {
            echo 'FAILED: Check the stage and console output.'
        }
    }
}
