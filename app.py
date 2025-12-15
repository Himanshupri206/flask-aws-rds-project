from flask import Flask, request, jsonify
import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_db_connection():
    conn = psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT,
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD
    )
    return conn

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status':'healthy'}), 200
    except Exception as e:
        return jsonify({'status:':'unthealthy', 'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
