pipeline {
    agent { label 'Worker-1' }

    triggers {
        cron('16 13 * * *')
    }

    stages {
        stage('Preparar script') {
            steps {
                sh 'chmod +x rutinasura.sh'
            }
        }

        stage('Ejecutar respaldo') {
            steps {
                sh './rutinasura.sh'
            }
        }

        stage('Finalizar') {
            steps {
                echo 'Rutina completada'
            }
        }
    }

    post {
        success {
            echo '✅ Correo Enviado con la rutina de rabbitmq de SUAPORTE Y SIMPLE /opt/adminarus'
        }
        failure {
            echo '❌ Algo salió mal durante la rutina'
        }
    }
}
