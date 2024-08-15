pipeline {
    agent any

    parameters {
        string(name: 'BRANCH_NAME', defaultValue: '', description: 'Branch to build')
        string(name: 'ENVIRONMENT', defaultValue: 'development', description: 'Deployment environment')
    }

    environment {
        // Define environment variables based on branch
        PORT = '8081'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from the specified branch
                script {
                    checkout([$class: 'GitSCM', 
                        branches: [[name: "${params.BRANCH_NAME}"]], 
                        userRemoteConfigs: [[url: 'https://github.com/novrian6/python_jenkins_demo.git']]
                    ])
                }
            }
        }
        
        stage('Build') {
            steps {
                echo "Building branch: ${params.BRANCH_NAME}"
                // Add build steps here
            }
        }
        
        stage('Test') {
            steps {
                echo "Testing branch: ${params.BRANCH_NAME}"
                // Add test steps here
            }
        }
        
        stage('Deploy') {
            when {
                expression { params.ENVIRONMENT == 'development' || params.ENVIRONMENT == 'staging' || params.ENVIRONMENT == 'production' }
            }
            steps {
                script {
                    // Adjust the port based on the environment
                    if (params.ENVIRONMENT == 'development') {
                        env.PORT = '8081'
                    } else if (params.ENVIRONMENT == 'staging') {
                        env.PORT = '8082'
                    } else if (params.ENVIRONMENT == 'production') {
                        env.PORT = '8083'
                    }
                    
                    // Deploy the application to the appropriate environment
                    echo "Deploying to ${params.ENVIRONMENT} on port ${env.PORT}"
                    sh "scp -i ~/.ssh/id_rsa -r * nn@172.16.137.133:/home/nn/flask_apps/${params.ENVIRONMENT}"
                    sh "ssh nn@172.16.137.133 'sudo systemctl restart flask_${params.ENVIRONMENT}.service'"
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

