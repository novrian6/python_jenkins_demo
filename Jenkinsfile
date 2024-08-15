pipeline {
    agent any
    environment {
        SSH_CREDENTIALS_ID = 'bc013f38-40d9-4731-8ed1-23c56055cc0f'
        SUDO_PASSWORD = credentials('sudo-password') // Replace with your credential ID
    }
    
    stages {
        stage('Add Host Key') {
            steps {
                sshagent(credentials: [SSH_CREDENTIALS_ID]) {
                    sh '''
                    ssh-keyscan -H 172.16.137.133 >> ~/.ssh/known_hosts
                    '''
                }
            }
        }
        
        stage('Checkout') {
            steps {
                script {
                    // Checkout the code from the current branch
                    checkout scm
                }
            }
        }
        
        stage('Build & Test') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                    // Uncomment to run tests
                    // sh 'pytest'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    def targetFolder
                    def serviceName

                    // Define deployment targets based on the branch name
                    if (env.BRANCH_NAME.startsWith('feature/')) {
                        // Feature branches are deployed to the development environment
                        targetFolder = '/home/nn/flask_apps/development'
                        serviceName = 'flask_development.service'
                    } else if (env.BRANCH_NAME == 'develop') {
                        // Develop branch is deployed to the staging environment
                        targetFolder = '/home/nn/flask_apps/staging'
                        serviceName = 'flask_staging.service'
                    } else if (env.BRANCH_NAME.startsWith('release/')) {
                        // Release branches are deployed to a separate pre-production environment
                        targetFolder = '/home/nn/flask_apps/preproduction'
                        serviceName = 'flask_preproduction.service'
                    } else if (env.BRANCH_NAME == 'master') {
                        // Master branch is deployed to the production environment
                        targetFolder = '/home/nn/flask_apps/production'
                        serviceName = 'flask_production.service'
                    } else {
                        error "Unknown branch: ${env.BRANCH_NAME}"
                    }

                    // Deploy the code to the target server
                    sshagent([env.SSH_CREDENTIALS_ID]) {
                        sh "scp -o StrictHostKeyChecking=no -r *.py requirements.txt nn@172.16.137.133:${targetFolder}"
                        sh """
                        echo ${SUDO_PASSWORD} | ssh -o StrictHostKeyChecking=no nn@172.16.137.133 'sudo -S systemctl restart ${serviceName}'
                        """
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
