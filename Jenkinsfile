pipeline {
    agent any

    stages {

        stage('Build Order Service') {
            steps {
                sh 'docker build -t order-service ./order-service'
            }
        }

        stage('Build Forecast Service') {
            steps {
                sh 'docker build -t forecast-service ./forecast-service'
            }
        }

        stage('Build Recommendation Service') {
            steps {
                sh 'docker build -t recommendation-service ./recommendation-service'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker run -d -p 5000:5000 order-service || true'
                sh 'docker run -d -p 5001:5001 forecast-service || true'
                sh 'docker run -d -p 5002:5002 recommendation-service || true'
            }
        }
    }
}
