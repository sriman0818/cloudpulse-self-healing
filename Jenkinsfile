
pipeline {

    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/sriman0818/cloudpulse-self-healing.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy Container') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
