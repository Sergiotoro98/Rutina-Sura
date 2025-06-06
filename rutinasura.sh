###BIN /BASH
echo Buenos dias,  > ${WORKSPACE}/${PIPELINE_NAME}/rabbitmq.log
echo Rutina operativa Rabbitmq > ${WORKSPACE}/${PIPELINE_NAME}/rabbitmq.log
date "+%Y-%m-%d %H:%M:%S" >> ${WORKSPACE}/${PIPELINE_NAME}/rabbitmq.log
/usr/local/bin/python3.11 ${WORKSPACE}/${PIPELINE_NAME}/rabbit.py >> ${WORKSPACE}/${PIPELINE_NAME}/rabbitmq.log
sleep 5
echo >> ${WORKSPACE}/${PIPELINE_NAME}/rabbitmq.log

echo Cordialmente >> ${WORKSPACE}/${PIPELINE_NAME}/rabbitmq.log

/usr/local/bin/python3.11 ${WORKSPACE}/${PIPELINE_NAME}/correo.py


