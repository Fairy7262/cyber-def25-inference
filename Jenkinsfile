pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // set this id in Jenkins
    IMAGE_NAME = "fairy7262/cyber-def25"
    TAG = "latest"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker --version || true'
        sh "docker build -t ${IMAGE_NAME}:${TAG} ."
      }
    }

    stage('Docker Hub Login') {
      steps {
        // login to docker hub using credentials stored in Jenkins
        sh '''
          echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
        '''
      }
    }

    stage('Push Image') {
      steps {
        sh "docker push ${IMAGE_NAME}:${TAG}"
      }
    }

    stage('Run with docker-compose') {
      steps {
        // Ensure docker-compose file exists in workspace; pull/push handled above
        sh '''
          docker-compose pull || true
          docker-compose up --abort-on-container-exit --exit-code-from inference
        '''
      }
    }
  }

  post {
    always {
      // Collect logs and workspace artifacts (optional)
      sh 'docker-compose down || true'
      archiveArtifacts artifacts: 'alerts.csv', allowEmptyArchive: true
    }
    success {
      echo "Pipeline completed successfully."
    }
    failure {
      echo "Pipeline failed — check logs."
    }
  }
}
