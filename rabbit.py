import requests
from requests.auth import HTTPBasicAuth

def get_rabbitmq_info(instances, user, password):
    results = {}
    for instance in instances:
        url = f"https://{instance}/api/overview"
        node_url = f"https://{instance}/api/nodes"

        try:
            response = requests.get(url, auth=HTTPBasicAuth(user, password), verify=False)
            node_response = requests.get(node_url, auth=HTTPBasicAuth(user, password), verify=False)

            if response.status_code == 200 and node_response.status_code == 200:
                data = response.json()
                nodes_data = node_response.json()  # Lista de nodos en el clúster

                nodes_info = []
                for node in nodes_data:
                    memoria_ram_bytes = node.get("mem_used", 0)
                    memoria_ram_mb = memoria_ram_bytes / (1024 ** 2)  # Convertir a MB
                    mem_limit_bytes = node.get("mem_limit", 0)
                    mem_limit_mb = mem_limit_bytes / (1024 ** 2)  # Convertir a MB
                    
                    # Calcular el porcentaje de uso de memoria
                    if mem_limit_mb > 0:
                        porcentaje_uso = (memoria_ram_mb / mem_limit_mb) * 100
                    else:
                        porcentaje_uso = 0

                    node_state = "Running" if node.get("running", False) else "Down"

                    nodes_info.append({
                        "nodo": node.get("name", "N/A"),
                        "Memoria_RAM": f"{memoria_ram_mb:.2f}MB",
                        "Memoria_Total": f"{mem_limit_mb:.2f}MB",
                        "Porcentaje_uso": f"{porcentaje_uso:.2f}%",
                        "Estado": node_state
                    })

                results[instance] = {
                    "Conexiones_Activas": data.get("object_totals", {}).get("connections", "N/A"),
                    "Mensajes_Totales": data.get("queue_totals", {}).get("messages", "N/A"),
                    "Mensajes_Listos": data.get("queue_totals", {}).get("messages_ready", "N/A"),
                    "Mensajes_No_Confirmados": data.get("queue_totals", {}).get("messages_unacknowledged", "N/A"),
                    "Consumidores": data.get("object_totals", {}).get("consumers", "N/A"),
                    "Nodos": nodes_info
                }
            else:
                results[instance] = {"error": f"HTTP {response.status_code} o {node_response.status_code}"}
        except Exception as e:
            results[instance] = {"error": str(e)}

    return results

if __name__ == "__main__":
    instances = [
        "mqcorppdn.suramericana.com",
        "rabbitmqcvconsolapdn.suramericana.com",
        "msg.suramericana.com.co",
        "msgss.suramericana.com.co"
    ]
    user = "admin_rabbit" 
    password = "5tfNkPcKSceRc8TD2xpg" 

    info = get_rabbitmq_info(instances, user, password)
    for instance, details in info.items():
        print(f"\nInstancia: {instance}")
        for key, value in details.items():
            if key == "Nodos":
                print("Nodos:")
                for node in value:
                    print(f"  - Nodo: {node['nodo']}, Memoria Utilizada: {node['Memoria_RAM']}, Porcentaje Memoria: {node['Porcentaje_uso']}, Estado_Nodo: {node['Estado']}")
            else:
                print(f"{key}: {value}")
