# Sensor humiddade e temperatura

Este projeto é um sistema de Internet das Coisas (IoT) projetado para monitorar a temperatura e a umidade usando um microcontrolador ESP8266 e um sensor DHT11. Os dados coletados são enviados para uma API Flask em execução em um Raspberry Pi, onde são armazenados em um banco de dados MySQL. Os dados podem ser acessados remotamente por meio de requisições HTTP GET.

### funcionalidades
- ESP8266: Lê a temperatura e a umidade do sensor DHT11 e envia os dados para a API Flask.
- API Flask: Recebe os dados do ESP8266, armazena-os em um banco de dados MySQL e fornece endpoints para recuperar os dados.
- Banco de Dados MySQL: Armazena os dados de temperatura e umidade junto com os carimbos de data e hora.
- Acesso Remoto: Os dados podem ser acessados remotamente por meio de requisições HTTP GET para a API Flask.

### componentes hardware
- ESP8266
- Sensor de Temperatura DHT11
- Jumpers e Protoboard
- Raspberry Pi

  
### componentes software
- Micropython
- Flask na Raspberry PI
- Banco de dados MySQL
- Biblioteca python para requests

## Instruções de configuração
- Flash MicroPython na ESP8266
- Enviar main.py para ESP usando ampy. ex:
ampy --port /dev/ttyUSB0 put main.py(assumindo que sua porta ultilizada seja a ttyUSB0)
- Executar o main.py no ESP. ex:
ampy --port /dev/ttyUSB0 run main.py
- Criar banco de dados e tabela no seu banco de dados:
CREATE DATABASE iot_data;
USE iot_data;
CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature VARCHAR(5),
    humidity VARCHAR(5),
    data_time DATETIME
);
- Criar arquivo app.py dentro da Raspberry instalar o Flask dentro da raspberry e executar com: Python3 app.py

### Acessando Dados
- A ESP enviará os dados para a API flask dentro da raspberry
- Todos Os dados podem ser acessados na rota 'GET  /data'
- a pesquisa tambem pode ser feita por id em 'GET  /data/id
- Para testar endpoints podem ser usadas ferramentes como Insomnia e Postman
