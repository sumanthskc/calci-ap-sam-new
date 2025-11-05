// Define the Docker image for the Continuous Integration (CI) stage
def PYTHON_IMAGE = 'python:3.12-slim'
// SAM_IMAGE definition removed, as requested.

pipeline {
    // We define specific agents for each stage
    agent none 

    stages {
        // --- Continuous Integration (CI) Stages ---

        stage('Source Checkout') {
            // Run on the default Jenkins agent
            agent any
            steps {
                echo 'Checking out code from Git...'
                // The pipeline automatically checks out the code based on the SCM configuration.
            }
        }

        stage('CI: Unit Tests') {
            // Use a Docker agent (python:3.9-slim) for a clean, consistent Python environment
            agent {
                docker {
                    image PYTHON_IMAGE
                    // Note: Removed the args line as it is rarely needed just for running unit tests.
                }
            }
            steps {
                echo 'Running unit tests...'
                // Run the unit tests (Step 3b)
                // If this fails, the pipeline stops here.
                sh 'python -m unittest test_calculator.py'
                
                echo 'Unit tests passed! Artifact preparation handled by SAM build later.'
            }
        }

        // --- Continuous Deployment (CD) Stages ---

        stage('CD: SAM Build and Deploy') {
            // Use 'agent any' to run the deployment commands directly on the Jenkins host/agent.
            // This assumes the host has SAM CLI, AWS CLI, and configured AWS credentials.
            agent any
            
            steps {
                echo 'Building SAM template for deployment...'
                // 1. Package the code/dependencies into the .aws-sam directory
                // SAM handles the building and packaging of the Python code into a Lambda-ready artifact.
                sh 'sam build'
                echo 'Deploying to AWS CloudFormation (CD Goal: deploy safely)...'
                // 2. Deploy the application, creating/updating the stack
                // IMPORTANT: Replace 'YOUR_S3_BUCKET' placeholder with a real S3 bucket name. 
                // SAM requires an S3 bucket to store the packaged code before deployment.
                sh 'sam deploy --template-file .aws-sam/build/template.yaml --stack-name CalculatorAppStack --capabilities CAPABILITY_IAM --no-confirm-changeset --region us-east-1 --resolve-s3'
            }
        }
    }

    post {
        always {
            // This closes the feedback loop, notifying the team of the pipeline's status.
            echo 'Pipeline finished.'
        }
        success {
            echo 'CI/CD Pipeline Succeeded! Application deployed to AWS.'
        }
        failure {
            echo 'CI/CD Pipeline Failed! Check the unit tests or deployment logs for details.'
        }
    }
}
