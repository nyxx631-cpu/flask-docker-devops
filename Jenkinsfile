pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nikhil031020/flask-docker-app"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Run Automated Tests') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                    python -m unittest test_app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                    docker build -t %DOCKER_IMAGE%:%IMAGE_TAG% -t %DOCKER_IMAGE%:latest .
                """
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %DOCKER_IMAGE%:%IMAGE_TAG%
                        docker push %DOCKER_IMAGE%:latest
                    """
                }
            }
        }

        stage('Deploy to Localhost') {
            steps {
                bat """
                    docker pull %DOCKER_IMAGE%:latest
                    docker stop flask-app || ver > nul
                    docker rm flask-app || ver > nul
                    docker run -d --name flask-app -p 5000:5000 --restart always %DOCKER_IMAGE%:latest
                """
            }
        }
    }

    post {
        always {
            bat 'docker logout || ver > nul'
        }
        success {
            echo "Pipeline succeeded! App is live at http://localhost:5000 and image pushed as ${DOCKER_IMAGE}:${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed. Check stage logs."
        }
    }
}
