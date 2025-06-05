pipeline {
    agent { label 'github-token-sergio' }
    
    triggers {
        // Ejecutar todos los días a las 2 AM
        cron('H 15 * * *')
    }

    stages {
        stage('Ejecutar respaldo') {
            steps {
                sh 'chmod +x rutina.sh'
                sh './rutina.sh'
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