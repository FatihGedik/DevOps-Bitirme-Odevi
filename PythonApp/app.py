from typing import List, Dict
from flask import Flask
import mysql.connector
import json

app = Flask(__name__)


def buyuk_sehirler() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'admin123',
        'host': 'mydb',
        'port': '3306',
        'database': 'sehirler'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM buyuk_sehirler')
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    return json.dumps({'buyuk_sehirler': buyuk_sehirler()})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
