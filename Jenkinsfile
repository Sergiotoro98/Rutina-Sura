pipeline {
    agent { label 'Worker-1' }
    
    triggers {
        // Ejecutar todos los días a las 2 AM
        cron('H 15 * * *')
    }

    stages {
        stage('Ejecutar respaldo') {
            steps {
                sh 'chmod +x rutinasura.sh'
                sh './rutinasura.sh'
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
