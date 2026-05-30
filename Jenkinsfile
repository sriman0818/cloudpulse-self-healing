pipeline {

agent any

stages {

    stage('Build Docker Image') {
        steps {
            sh 'docker compose build'
        }
    }

    stage('Deploy Container') {
        steps {
            sh 'docker compose down || true'
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
