import machine
import time
import network
import ntptime
import dht
import ujson
import urequests as requests

# Configura o pino GPIO4 (D2) como entrada para o sensor
sensor = dht.DHT11(machine.Pin(4))  

# Configuração da rede Wi-Fi 
SSID = "SEU_NOME_WIFI"
PASSWORD = "SUA_SENHA_WIFI"

# URL da API
api_url = 'http://LOCALHOST:9898/add'
headers = {'Content-Type': 'application/json'}

# Função para conectar à rede Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando à rede Wi-Fi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Conectado com sucesso à rede Wi-Fi')
    print('Configurando hora via NTP...')
    ntptime.settime()
    print('Hora configurada com sucesso via NTP')

# Conecta à rede Wi-Fi
connect_wifi()

while True:
    try:
        sensor.measure()  # Mede a temperatura e umidade
        temp = sensor.temperature()  # Obtém a temperatura
        hum = sensor.humidity()  # Obtém a umidade

        # Obtém a hora local atual
        current_time = time.localtime()
        formatted_time = '{:04}-{:02}-{:02} {:02}:{:02}:{:02}'.format(current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5])

        print('Time: {}, Temperature: {}°C, Humidity: {}%'.format(formatted_time, temp, hum))

        # Cria o JSON com os dados
        data = {
            'temperature': temp,
            'humidity': hum,
            'time': formatted_time
        }
        json_data = ujson.dumps(data)
        print('Dados JSON:', json_data)

        # Envia os dados para a API
        response = requests.post(api_url, data=json_data, headers=headers)
        print('Resposta da API:', response.json())
        response.close()

    except OSError as e:
        print('Failed to read sensor.')

    time.sleep(3600)  # Aguarda 3600 segundos (1 hora) antes da próxima leitura
