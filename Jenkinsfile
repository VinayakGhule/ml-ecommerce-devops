pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/VinayakGhule/ml-ecommerce-devops.git'
            }
        }

        stage('Build Containers') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Run Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
