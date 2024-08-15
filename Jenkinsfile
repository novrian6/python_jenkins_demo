pipeline {
    agent any
    environment {
        // Define SSH credentials ID here
        SSH_CREDENTIALS_ID = 'your-ssh-credentials-id'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/novrian6/python_jenkins_demo.git'
            }
        }
        stage('Build & Test') {
            steps {
                script {
                    // Install dependencies and run tests
                    sh 'pip install -r requirements.txt'
                    sh 'pytest'
                }
            }
        }
        stage('Deploy to Staging') {
            when {
                branch 'development'
            }
            steps {
                script {
                    sshagent([env.SSH_CREDENTIALS_ID]) {
                        sh 'scp -r * nn@172.16.137.133:/home/nn/flask_apps/staging'
                        sh 'ssh nn@172.16.137.133 "cd /home/nn/flask_apps/staging && ./deploy.sh"'
                    }
                }
            }
        }
        stage('Approval') {
            steps {
                input 'Approve deployment to Production?'
            }
        }
        stage('Deploy to Production') {
            when {
                branch 'master'
            }
            steps {
                script {
                    sshagent([env.SSH_CREDENTIALS_ID]) {
                        sh 'scp -r * nn@172.16.137.133:/home/nn/flask_apps/production'
                        sh 'ssh nn@172.16.137.133 "cd /home/nn/flask_apps/production && ./deploy.sh"'
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}

