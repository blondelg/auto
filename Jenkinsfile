pipeline {
    agent any

    stages {
        stage('Build') {
            steps{
                sh 'mkdir auto'
                dir('auto'){
                    git 'https://github.com/blondelg/auto.git'
                    sh 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
                    sh 'python3.8 get-pip.py'
                    sh '/var/lib/jenkins/.local/bin/pip install -r requirements.txt'
                }
                dir('auto/auto'){
                    sh 'cp config_sample.ini config.ini'
                    sh 'sed -i "s/SECRET_KEY_PATTERN/$(python3.8 ../generate_key.py)/gI" config.ini'
                }
            }
        }
        stage('Test') {
            steps{
                dir('auto'){
                    sh 'python3.8 manage.py test'
                }
            }
        }
        stage('Run') {
            steps{
                dir('auto'){
                    sh 'pwd'
                    sh 'JENKINS_NODE_COOKIE=dontKillMe nohup /usr/bin/python3.8 manage.py runserver 0.0.0.0:8000 &'
                }
            }
        }
    }
}
