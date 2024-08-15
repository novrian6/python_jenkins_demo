pipeline {
    agent any
    environment {
        SSH_CREDENTIALS_ID = 'bc013f38-40d9-4731-8ed1-23c56055cc0f'
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
                git branch: "${env.BRANCH_NAME}", url: 'https://github.com/novrian6/python_jenkins_demo.git'
            }
        }
        stage('Build & Test') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                    //sh 'pytest'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    def targetFolder
                    def serviceName

                    if (env.BRANCH_NAME == 'development') {
                        targetFolder = '/home/nn/flask_apps/development'
                        serviceName = 'flask_development.service'
                    } else if (env.BRANCH_NAME == 'staging') {
                        targetFolder = '/home/nn/flask_apps/staging'
                        serviceName = 'flask_staging.service'
                    } else if (env.BRANCH_NAME == 'master') {
                        targetFolder = '/home/nn/flask_apps/production'
                        serviceName = 'flask_production.service'
                    } else {
                        error "Unknown branch: ${env.BRANCH_NAME}"
                    }

                    sshagent([env.SSH_CREDENTIALS_ID]) {
                        sh "scp -o StrictHostKeyChecking=no -r *.py requirements.txt nn@172.16.137.133:${targetFolder}"
                       // sh "ssh -o StrictHostKeyChecking=no nn@172.16.137.133 'sudo systemctl restart ${serviceName}'"
                        echo 'P@ssword' | ssh -o StrictHostKeyChecking=no nn@172.16.137.133 'sudo -S systemctl restart ${serviceName}'
                      
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
