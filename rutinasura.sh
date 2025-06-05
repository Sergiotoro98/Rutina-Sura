###BIN /BASH

echo Buenos dias,  > /opt/automatizacion/rabbit-EO/rabbitmq.log
echo Rutina operativa Rabbitmq > /opt/automatizacion/rabbit-EO/rabbitmq.log 
date "+%Y-%m-%d %H:%M:%S" >> /opt/automatizacion/rabbit-EO/rabbitmq.log
/usr/local/bin/python3.11 /opt/automatizacion/rabbit-EO/rabbit.py >> /opt/automatizacion/rabbit-EO/rabbitmq.log
sleep 5
echo >> /opt/automatizacion/rabbit-EO/rabbitmq.log

echo Cordialmente >> /opt/automatizacion/rabbit-EO/rabbitmq.log

/usr/local/bin/python3.11 /opt/automatizacion/rabbit-EO/correo.py

