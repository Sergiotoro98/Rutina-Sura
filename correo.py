import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

def parse_log(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    instance_data = {}
    nodes = []

    for line in lines:
        line = line.strip()

        if line.startswith("Instancia:"):
            if instance_data:
                instance_data["Nodos"] = nodes
                data.append(instance_data)
                instance_data = {}
                nodes = []
            instance_data["Instancia"] = line.split(": ")[1]
        elif line.startswith("Conexiones_Activas:"):
            instance_data["Conexiones Activas"] = int(line.split(": ")[1])
        elif line.startswith("Mensajes_Totales:"):
            instance_data["Mensajes Totales"] = int(line.split(": ")[1])
        elif line.startswith("Mensajes_Listos:"):
            instance_data["Mensajes Listos"] = int(line.split(": ")[1])
        elif line.startswith("Mensajes_No_Confirmados:"):
            instance_data["Mensajes No Confirmados"] = int(line.split(": ")[1])
        elif line.startswith("Consumidores:"):
            instance_data["Consumidores"] = int(line.split(": ")[1])
        elif line.startswith("- Nodo:"):
            match = re.match(r"- Nodo: (.*?), Memoria Utilizada: (\d+\.\d+)MB, Porcentaje Memoria: (\d+\.\d+)%, Estado_Nodo: (\w+)", line)
            if match:
                nodes.append({
                    "Nodo": match.group(1),
                    "Memoria Utilizada (MB)": float(match.group(2)),
                    "Porcentaje Memoria (%)": float(match.group(3)),
                    "Estado Nodo": match.group(4)
                })

    if instance_data:
        instance_data["Nodos"] = nodes
        data.append(instance_data)

    return data

def generate_html(data):
    html_content = """
    <html>
    <head>
        <title>Reporte RabbitMQ</title>
        <style>
            table { width: 100%%; border-collapse: collapse; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .green { background-color: #c3e6cb; } /* Verde */
            .yellow { background-color: #ffeeba; } /* Amarillo */
            .red { background-color: #f5c6cb; } /* Rojo */
        </style>
    </head>
    <body>
    <h1>Reporte RabbitMQ</h1>
    """

    for inst in data:
        html_content += f"<h2>{inst['Instancia']}</h2>"
        html_content += "<p><strong>Conexiones Activas:</strong> {}<br>".format(inst.get("Conexiones Activas", "N/A"))
        html_content += "<strong>Mensajes Totales:</strong> {}<br>".format(inst.get("Mensajes Totales", "N/A"))
        html_content += "<strong>Mensajes Listos:</strong> {}<br>".format(inst.get("Mensajes Listos", "N/A"))
        html_content += "<strong>Mensajes No Confirmados:</strong> {}<br>".format(inst.get("Mensajes No Confirmados", "N/A"))
        html_content += "<strong>Consumidores:</strong> {}</p>".format(inst.get("Consumidores", "N/A"))

        html_content += "<table><tr><th>Nodo</th><th>Memoria Utilizada (MB)</th><th>Porcentaje Memoria (%)</th><th>Estado Nodo</th></tr>"

        for node in inst['Nodos']:
            mem_percentage = node['Porcentaje Memoria (%)']
            estado_nodo = node['Estado Nodo']

            # Definir color para el estado del nodo
            estado_color = "green" if estado_nodo.lower() == "running" else ""

            # Definir color para el porcentaje de memoria
            if mem_percentage < 50:
                mem_color = "green"
            elif 50 <= mem_percentage <= 79:
                mem_color = "yellow"
            else:
                mem_color = "red"

            html_content += f"""
                <tr>
                    <td>{node['Nodo']}</td>
                    <td>{node['Memoria Utilizada (MB)']}</td>
                    <td class="{mem_color}">{node['Porcentaje Memoria (%)']}</td>
                    <td class="{estado_color}">{node['Estado Nodo']}</td>
                </tr>
            """

        html_content += "</table>"

    html_content += """</body></html>"""
    return html_content

def send_email(html_content, sender_email, receiver_email, smtp_server, smtp_port):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Reporte RabbitMQ"
    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Configuración
log_file = "/opt/ansible/rabbitsura/surarabbitmq.log"
sender_email = "rutinasura@arus.com.co"
receiver_email = "servidores_aplicaciones@arus.com.co"
smtp_server = "10.0.0.30"
smtp_port = 25  # Cambiar si el relay usa otro puerto

data = parse_log(log_file)
html_report = generate_html(data)
send_email(html_report, sender_email, receiver_email, smtp_server, smtp_port)

print("Correo enviado con el reporte HTML.")

