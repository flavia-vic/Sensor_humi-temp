import dht
import machine
import time
import utime
import network
import ntptime

# Configura o pino GPIO4 (D2) como entrada para o sensor
sensor = dht.DHT11(machine.Pin(4))  

# Configuração da rede Wi-Fi 
SSID = "Daileon 2G"
PASSWORD = "Mimouzinho123"

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
        current_time = utime.localtime()
        formatted_time = '{:02}:{:02}:{:02}'.format(current_time[3], current_time[4], current_time[5])

        print('Time: {}, Temperature: {}°C, Humidity: {}%'.format(formatted_time, temp, hum))

    except OSError as e:
        print('Failed to read sensor.')

    time.sleep(2)  # Aguarda 2 segundos antes da próxima leitura
