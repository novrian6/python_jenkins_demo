pipeline {
    agent any
    environment {
        SSH_CREDENTIALS_ID = 'targetserver' // SSH credentials ID for the target server
        SUDO_PASSWORD = credentials('sudo-password') // Replace with your sudo-password credential ID if needed
    }

    stages {
        stage('Add Host Key') {
            steps {
                sshagent(credentials: [SSH_CREDENTIALS_ID]) {
                    script {
                        // Debugging step: Check the SSH keyscan output
                        echo "Adding target server to known hosts..."
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
                    echo "Checking out code from Git repository"
                    checkout scm
                }
            }
        }

        stage('Build & Test') {
            steps {
                script {
                    echo "Installing dependencies..."
                    sh 'pip install -r requirements.txt'
                    // Uncomment to run tests if needed
                    // echo "Running tests..."
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

                    // Debugging: Output branch and server configuration
                    echo "Branch: ${env.BRANCH_NAME}"

                    // Define deployment targets based on the branch name
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

                    // Debugging: Output the deployment target details
                    echo "Deploying to ${serverAddress} at ${targetFolder}"

                    // Deploy the code to the target server
                    sshagent([SSH_CREDENTIALS_ID]) {
                        sh """
                        ssh ${SSH_CREDENTIALS_ID} ${serverAddress} 'mkdir -p ${targetFolder}'
                        scp -r ./ ${SSH_CREDENTIALS_ID}@${serverAddress}:${targetFolder}
                        ssh ${SSH_CREDENTIALS_ID} ${serverAddress} 'systemctl restart ${serviceName}'
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            node {
                // Clean up workspace after the pipeline is complete
                echo "Cleaning up workspace..."
                cleanWs()
            }
        }

        success {
            echo "Build and deployment succeeded!"
        }

        failure {
            echo "Build or deployment failed. Please check the logs."
        }
    }
}
