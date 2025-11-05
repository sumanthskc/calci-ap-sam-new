// Defines the Docker image used for the Continuous Integration (CI) stage.
def PYTHON_IMAGE = 'python:3.12-slim' 

// IMPORTANT: Replace 'aws-deploy-user' with the ID you used when saving your AWS credentials in Jenkins.
// This ID MUST be set up in Manage Jenkins -> Manage Credentials first.
def AWS_CREDENTIALS_ID = 'd73f4e59-80ab-438d-aacb-4b271a4cacb3' 

pipeline {
    // We define specific agents per stage
    agent none 

    stages {
        stage('1. Source Checkout') {
            agent any
            steps {
                echo 'CI Stage 1: Checking out code from Git...'
            }
        }

        stage('2. CI: Unit Tests') {
            // Runs tests inside a consistent Docker environment (CI Goal: repeatable environment)
            // Requires the 'Docker Pipeline' plugin in Jenkins.
            agent {
                docker {
                    image PYTHON_IMAGE
                }
            }
            steps {
                echo 'CI Stage 2: Running unit tests inside Docker container.'
                sh 'python -m unittest test_calculator.py'
                echo 'Unit tests passed successfully.'
            }
        }

        stage('3. CD: SAM Build and Deploy') {
            // This stage runs on the Jenkins host where SAM/AWS CLI must be installed.
            agent {
                docker {
                    // Use the same Python base image
                    image PYTHON_IMAGE
                    // If permissions are an issue (common for Docker-in-Docker type use cases):
                    // args '-v /var/run/docker.sock:/var/run/docker.sock' 
                }
            }
            
            steps {
                echo 'CD Stage 3: Installing SAM CLI inside Docker container...'
                // Install SAM CLI and its dependencies inside the running container environment
                sh 'pip install awscli aws-sam-cli'

                echo 'Starting SAM build process.'
                
                sh 'sam build --template-file template.yaml'

                echo 'Deploying to AWS CloudFormation via SAM CLI (Resolving S3 Automatically)...'
                
                // CRITICAL FIX: The withCredentials block securely exposes the AWS keys 
                // as environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) 
                // for the SAM CLI command to use for authentication, resolving the 'Unable to locate credentials' error.
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, variablePrefix: 'AWS')]) {
                    sh 'sam deploy --template-file .aws-sam/build/template.yaml ' +
                       '--stack-name CalculatorAppStack ' +
                       '--capabilities CAPABILITY_IAM ' +
                       '--no-confirm-changeset ' +
                       '--resolve-s3 ' + // Automatically manages the S3 bucket for staging
                       '--region us-east-1 '
                }
                
                echo 'CD Goal Achieved: Code deployment triggered to AWS cloud.'
            }
        }
    }

    post {
        always {
            echo 'Pipeline job finished. [cite_start](CI Goal: close feedback loop [cite: 37])'
        }
        success {
            echo 'SUCCESS: CI/CD Pipeline completed. Calculator app is deploying to AWS Lambda/API Gateway.'
        }
        failure {
            echo 'FAILURE: Pipeline execution failed. Check logs for test failures or deployment errors.'
        }
    }
}
