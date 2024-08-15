pipeline {
    agent any

    environment {
        // Default port and environment
        PORT = ''
        ENVIRONMENT = ''
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Automatically use the branch currently being built
                    def branchName = env.BRANCH_NAME
                    
                    // Set environment and port based on the branch
                    switch (branchName) {
                        case 'master':
                            env.ENVIRONMENT = 'production'
                            env.PORT = '8083'
                            break
                        case 'staging':
                            env.ENVIRONMENT = 'staging'
                            env.PORT = '8082'
                            break
                        case 'development':
                        default:
                            env.ENVIRONMENT = 'development'
                            env.PORT = '8081'
                            break
                    }
                    
                    // Checkout code from the current branch
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "${branchName}"]], 
                        userRemoteConfigs: [[url: 'https://github.com/novrian6/python_jenkins_demo.git']]
                    ])
                }
            }
        }
        
        stage('Build') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME} in environment: ${env.ENVIRONMENT}"
                // Add build steps here
            }
        }
        
        stage('Test') {
            steps {
                echo "Testing branch: ${env.BRANCH_NAME} in environment: ${env.ENVIRONMENT}"
                // Add test steps here
            }
        }
        
        stage('Deploy') {
            when {
                expression { env.ENVIRONMENT == 'development' || env.ENVIRONMENT == 'staging' || env.ENVIRONMENT == 'production' }
            }
            steps {
                script {
                    echo "Deploying to ${env.ENVIRONMENT} on port ${env.PORT}"
                    
                    // Deploy the application to the appropriate environment
                    sh "scp -i ~/.ssh/id_rsa -r * nn@172.16.137.133:/home/nn/flask_apps/${env.ENVIRONMENT}"
                    sh "ssh nn@172.16.137.133 'sudo systemctl restart flask_${env.ENVIRONMENT}.service'"
                }
            }
        }
    }
    
    post {
        always {
            echo "Cleaning up"
            // Add cleanup steps if necessary
        }
    }
}
