pipeline {
    agent any
    environment {
        SSH_CREDENTIALS_ID = 'targetserver' // Use your actual SSH credential ID here
    }
    
    stages {
        stage('Add Host Key') {
            steps {
                sshagent(credentials: [SSH_CREDENTIALS_ID]) {
                    script {
                        sh '''
                        ssh-keyscan -H development.server.com >> ~/.ssh/known_hosts
                        ssh-keyscan -H staging.server.com >> ~/.ssh/known_hosts
                        ssh-keyscan -H preproduction.server.com >> ~/.ssh/known_hosts
                        ssh-keyscan -H production.server.com >> ~/.ssh/known_hosts
                        '''
                    }
                }
            }
        }
        
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }
        
        stage('Build & Test') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                    // Uncomment to run tests if needed
                    // sh 'pytest'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    def targetFolder
                    def serviceName
                    def serverAddress

                    if (env.BRANCH_NAME.startsWith('feature/')) {
                        targetFolder = '/home/nn/flask_apps/development'
                        serviceName = 'flask_development.service'
                        serverAddress = 'development.server.com'
                    } else if (env.BRANCH_NAME == 'develop') {
                        targetFolder = '/home/nn/flask_apps/staging'
                        serviceName = 'flask_staging.service'
                        serverAddress = 'staging.server.com'
                    } else if (env.BRANCH_NAME.startsWith('release/')) {
                        targetFolder = '/home/nn/flask_apps/preproduction'
                        serviceName = 'flask_preproduction.service'
                        serverAddress = 'preproduction.server.com'
                    } else if (env.BRANCH_NAME == 'master') {
                        targetFolder = '/home/nn/flask_apps/production'
                        serviceName = 'flask_production.service'
                        serverAddress = 'production.server.com'
                    } else {
                        error "Unknown branch: ${env.BRANCH_NAME}"
                    }

                    // Deploy to the target server
                    sshagent([env.SSH_CREDENTIALS_ID]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${serverAddress} "deploy commands here"
                        """
                    }
                }
            }
        }
    }
}
