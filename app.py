from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='seu_usuario',
        password='sua_senha',
        database='database'
    )

def insert_data(temperature, humidity, date_time):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO data_logs (temperature, humidity, data_time) VALUES (%s, %s, %s)',
            (temperature, humidity, date_time)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return "Success"
    except Exception as e:
        return str(e)

@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    temperature = data['temperature']
    humidity = data['humidity']
    date_time = data['time']
    result = insert_data(temperature, humidity, date_time)
    if result == "Success":
        return jsonify({'message': 'Data inserted successfully!'})
    else:
        return jsonify({'error': result})

@app.route('/data', methods=['GET'])
def get_all_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM data_logs')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM data_logs WHERE id = %s', (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if data is None:
        return jsonify({'error': 'Data not found'}), 404
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
