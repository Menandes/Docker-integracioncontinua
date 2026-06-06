pipeline {
    agent any

    environment {
        IMAGE_NAME           = 'flask-redis-app'
        IMAGE_TAG            = "${env.BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = 'flaskredis-ci'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                // Construye la imagen de app usando Dockerfile
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Smoke test') {
            steps {
                sh '''
                    set -e

                    echo "Levantando el stack (web + redis)..."
                    docker compose up -d --no-build

                    echo "Esperando a que la web escuche en :5000..."
                    ok=
                    for i in $(seq 1 15); do
                        if docker compose exec -T web python -c \
                            "import socket; socket.create_connection(('127.0.0.1', 5000), 2)" \
                            >/dev/null 2>&1; then
                            ok=1; echo "Web OK"; break
                        fi
                        sleep 2
                    done
                    if [ -z "$ok" ]; then
                        echo "La web no respondió a tiempo. Logs:"
                        docker compose logs
                        exit 1
                    fi

                    echo "Verificando Redis..."
                    if docker compose exec -T redis redis-cli ping | grep -q PONG; then
                        echo "Redis OK"
                    else
                        echo "Redis no respondió. Logs:"
                        docker compose logs
                        exit 1
                    fi
                '''
            }
        }

        // Acá irían test unitarios...
        // stage('Tests') {
        //     agent { docker { image 'python:3.11-slim'; reuseNode true } }
        //     steps {
        //         sh '''
        //             python -m pip install --upgrade pip
        //             pip install -r app/requerimientos.txt pytest
        //             pytest -q
        //         '''
        //     }
        // }
    }

    post {
        always {
            sh 'docker compose down -v || true'
            sh 'docker image prune -f || true'
        }
        success {
            echo "OK ✅  ${IMAGE_NAME}:${IMAGE_TAG} construida y verificada."
        }
        failure {
            echo "Build falló ❌  — revisa el log del stage."
        }
    }
}