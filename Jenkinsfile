pipeline {
    agent any 
    environment {
        registryCredential = 'docker-hub-creds'
        imageName = 'kcgjr/pythonclient'
        dockerImage = ''
        }
    stages {
        stage('Run the tests') {
            agent {
                docker { 
                    image 'python:3.9'
                    // args '-e HOME=/tmp -e NPM_CONFIG_PREFIX=/tmp/.npm'
                    // reuseNode true
                }
            }
            steps {
                echo 'Retrieve source from github.'
				git branch: 'main',
					url: 'https://github.com/kgangideloitte/external_app_py.git'
				echo 'Do I have the files?'
				sh "ls -la"
				echo 'Run python install requirements'
				sh "pip install --user -r requirements.txt"
				echo 'Run python test'
				sh "python test_app.py" 
            }
        }
        stage('SonarQube analysis') {
            steps {
                script {
                def scannerHome = tool 'SonarQube-Scanner';
                    withSonarQubeEnv() {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Building image') {
            steps{
                script {
                    echo 'build the image'
					sh 'docker --version'
					dockerImage = docker.build imageName
				// 	sh 'docker build -t $imageName:$BUILD_NUMBER .'
					sh 'docker images' 
                }
            }
            }
        stage('Push Image') {
            steps{
                script {
                    echo 'push the image to docker hub'
					docker.withRegistry( '', registryCredential ) {
						dockerImage.push("v$BUILD_NUMBER")
					}
                }
            }
        }     
        stage('deploy to k8s') {
            agent {
                docker { 
                    image 'google/cloud-sdk:latest'
                    args '-e HOME=/tmp'
                    reuseNode true
                }
            }
            steps {
                echo 'Get credentails'
                // sh 'gcloud container clusters get-credentials kgangi-cluster --zone us-central1-b --project dtc-102021-u108'
                // sh 'kubectl set image deployment/events-internal events-internal=$imageName:v$BUILD_NUMBER --record'
            }
        }     
        stage('Remove local docker image') {
            steps{
                sh "docker rmi $imageName:latest"
                sh "docker rmi $imageName:v$BUILD_NUMBER"
            }
        }
    }
}
