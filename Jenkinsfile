pipeline {
    agent any

    environment {
        DOCKER_REGISTRY_URL = 'localhost:5000'
        IMAGE_BASE_NAME = 'open-market'
        DEPLOYMENT_NAME = 'open-market-api'
        NAMESPACE = 'default'
    }

    stages {
        stage('test') {
            steps {
                sh 'docker-compose build'
                sh 'docker-compose run --entrypoint make api test'
            }

            post{
                always{
                    cobertura   coberturaReportFile: 'coverage.xml',
                                conditionalCoverageTargets: '85, 0, 0',
                                enableNewApi: false,
                                lineCoverageTargets: '90, 0, 0',
                                maxNumberOfBuilds: 10,
                                methodCoverageTargets: '90, 0, 0',
                                sourceEncoding: 'ASCII',
                                zoomCoverageChart: false
                    junit 'junit.xml'
                    sh 'docker-compose down'
                }
            }

        }

        stage('build'){
            when { 
                branch 'master'
            } 
            steps {
                sh 'docker build -t $DOCKER_REGISTRY_URL/$IMAGE_BASE_NAME:$GIT_COMMIT .'
                sh 'docker push $DOCKER_REGISTRY_URL/$IMAGE_BASE_NAME:$GIT_COMMIT'
            }
        }

        stage('deploy'){
            when {
                branch 'master'
            }
            steps {
                sh 'kubectl --record deployment.apps/$DEPLOYMENT_NAME \
                            set image deployment.v1.apps/$DEPLOYMENT_NAME \
                            template-app-api=$DOCKER_REGISTRY_URL/$IMAGE_BASE_NAME:$GIT_COMMIT \
                            migrations=$DOCKER_REGISTRY_URL/$IMAGE_BASE_NAME:$GIT_COMMIT -n $NAMESPACE'
            }
        }

    }

}