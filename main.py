import network
import urequests
import time
from machine import Pin
import dht

# Configuração do sensor
sensor = dht.DHT11(Pin(4))

# Função para conectar à rede Wi-Fi
def connect_wifi():
    ssid = 'SEU_NOME_WIFI'
    password = 'SUA_SENHA_WIFI'
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
    print("Conectado com sucesso à rede Wi-Fi")

# Função para configurar a hora via NTP
def set_time_ntp():
    import ntptime
    ntptime.settime()
    print("Hora configurada com sucesso via NTP")

# Função para ler o sensor
def read_sensor():
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except OSError as e:
        print("Failed to read sensor.")
        return None, None

# Função para enviar dados para a API
def send_data(temperature, humidity, date_time):
    url = "http://LOCALHOST:5000/add"
    data = {
        "temperature": temperature,
        "humidity": humidity,
        "time": date_time
    }
    headers = {'Content-Type': 'application/json'}
    response = urequests.post(url, json=data, headers=headers)
    print("Dados JSON:", data)
    print("Resposta da API:", response.json())

# Conectando ao Wi-Fi
connect_wifi()

# Configurando hora via NTP
set_time_ntp()

# Loop principal para enviar dados a cada 1 hora
while True:
    temperature, humidity = read_sensor()
    if temperature is not None and humidity is not None:
        current_time = time.localtime()
        date_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            current_time[0], current_time[1], current_time[2],
            current_time[3], current_time[4], current_time[5]
        )
        send_data(temperature, humidity, date_time)
    time.sleep(3600)  # Esperar 1 hora (3600 segundos) antes de enviar os dados novamente
