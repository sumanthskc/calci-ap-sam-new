// Defines the Docker image used for the Continuous Integration (CI) stage.
def PYTHON_IMAGE = 'python:3.12-slim' 

// IMPORTANT: Replace 'aws-deploy-user' with the ID you used when saving your AWS credentials in Jenkins.
// This ID MUST be set up in Manage Jenkins -> Manage Credentials first.
def AWS_CREDENTIALS_ID = '4b45ce94-9f38-4058-b72a-b1241d2b068c' 

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

        stage('2. CI: Unit Tests (Docker Agent)') {
            // Runs tests inside a consistent, isolated Docker environment
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

        stage('3. CD: SAM Build and Deploy (Host Shell)') {
            // CRITICAL CHANGE: Use agent any to run commands directly on the host shell.
            // This requires SAM CLI and AWS CLI to be installed and accessible on the Jenkins host.
            agent any
            
            steps {
                echo 'CD Stage 3: Starting SAM build process on host shell.'
                // 1. Build: Prepare the deployment artifact
                sh 'sam build --template-file template.yaml'

                echo 'Deploying to AWS CloudFormation via SAM CLI (Resolving S3 Automatically)...'
                
                // 2. Deployment: Securely exposes credentials to the host shell environment
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, variablePrefix: 'AWS')]) {
                    sh 'sam deploy --template-file .aws-sam/build/template.yaml ' +
                       '--stack-name CalculatorAppStack ' +
                       '--capabilities CAPABILITY_IAM ' +
                       '--no-confirm-changeset ' +
                       '--resolve-s3 ' + // Automatically manages the S3 bucket for staging
                       '--region ap-south-1 '
                }
                
                echo 'CD Goal Achieved: Code deployment triggered to AWS cloud.'
            }
        }
    }

    post {
        always {
            echo 'Pipeline job finished. (CI Goal: close feedback loop)[cite_start]' [cite: 37]
        }
        success {
            echo 'SUCCESS: CI/CD Pipeline completed. Calculator app is deploying to AWS Lambda/API Gateway.'
        }
        failure {
            echo 'FAILURE: Pipeline execution failed. Check logs for test failures or deployment errors.'
        }
    }
}
