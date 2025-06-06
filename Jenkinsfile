pipeline {
    agent { label 'Worker-1' }

    triggers {
        cron('H 15 * * *') // 2 AM hora Colombia
    }

    stages {
        stage('Preparar entorno') {
            steps {
                sh 'chmod +x rutinasura.sh'
            }
        }

        stage('Ejecutar respaldo') {
            steps {
                sh './rutinasura.sh'
            }
        }

        stage('Verificar resultados') {
            steps {
                sh 'echo "Verificación completa"' // Aquí podrías agregar validaciones
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
