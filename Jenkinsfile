pipeline {
    agent any

    environment {
        // Replace with your actual Docker Hub username:
        DOCKER_HUB_USER = 'YOUR_DOCKERHUB_USERNAME'
        IMAGE_NAME      = "${DOCKER_HUB_USER}/devops-lab-app"
        IMAGE_TAG       = "${BUILD_NUMBER}"
    }

    stages {
        stage('Unit Testing') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    pip install --no-cache-dir -r requirements.txt
                    pytest test_app.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Push to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            sh "docker rmi -f ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest || true"
        }
        success {
            echo "CI pipeline completed successfully. Image pushed: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "CI pipeline failed. Inspect console logs."
        }
    }
}
