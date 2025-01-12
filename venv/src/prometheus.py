from prometheus_client import start_http_server, Gauge
import time
import random

# Criando uma métrica Gauge para o valor dos sensores
# A métrica terá labels como 'station_id' (ID da estação) e 'sensor_type' (tipo de sensor)
SENSOR_VALUE = Gauge('sensor_value', 'Sensor value over time', ['station_id', 'sensor_type'])

# Função para simular a leitura do sensor
def read_sensor(station_id, sensor_type):
    # Simulando um valor aleatório para o sensor (por exemplo, temperatura entre 18 e 30)
    sensor_value = random.uniform(18, 30) if sensor_type == 'temperature' else random.uniform(30, 90)
    return sensor_value

# Função para atualizar os valores dos sensores
def update_sensor_values():
    # Suponhamos que você tenha 3 estações e cada estação tenha 3 sensores
    stations = ['station_1', 'station_2', 'station_3']
    sensor_types = ['temperature', 'humidity', 'pressure']
    
    for station in stations:
        for sensor_type in sensor_types:
            value = read_sensor(station, sensor_type)
            # Atualiza a métrica com o valor do sensor e as labels (station_id e sensor_type)
            SENSOR_VALUE.labels(station_id=station, sensor_type=sensor_type).set(value)
            print(f"Sensor ({station}, {sensor_type}) - Valor: {value}")
    
if __name__ == '__main__':
    # Inicia o servidor HTTP para expor as métricas
    start_http_server(8000)  # O Prometheus vai acessar as métricas neste endpoint
    
    while True:
        # Atualiza os valores dos sensores a cada 10 segundos
        update_sensor_values()
        time.sleep(10)
