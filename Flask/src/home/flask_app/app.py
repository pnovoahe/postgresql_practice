import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response

db_host = os.getenv("POSTGRES_HOST", "postgres")
db_name = os.getenv("POSTGRES_DB", "myhome")
db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD", "admin123")

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host=db_host,
        	database=db_name,
		user=db_user,
        password=db_password)
    return conn


@app.route('/')
def index():
    endpoints = [
        {
            'name': 'Get Average Temperature of All Rooms',
            'url': '/get_avg_temp_of_all_rooms',
            'method': 'GET',
            'description': 'Returns the average temperature of all rooms.'
        },
        {
            'name': 'Get Average Temperature by Rooms',
            'url': '/get_avg_temp_by_rooms',
            'method': 'GET',
            'description': 'Returns the average temperature for each room.'
        },
        {
            'name': 'Get Maximum Temperature by Rooms',
            'url': '/get_max_temp_by_rooms',
            'method': 'GET',
            'description': 'Returns the maximum temperature recorded for each room.'
        },
        {
            'name': 'Get Room Name from ID',
            'url': '/get_room_name_from_id/<int:room_id>',
            'method': 'GET',
            'description': 'Returns the name of a room given its ID.'
        },
        {
            'name': 'Get Average Temperature from Room ID',
            'url': '/get_room_avg_temp_from_id/<int:room_id>',
            'method': 'GET',
            'description': 'Returns the average temperature for a room given its ID.'
        },
        {
            'name': 'Get Minimum Temperature from Room ID',
            'url': '/get_room_min_temp_from_id/<int:room_id>',
            'method': 'GET',
            'description': 'Returns the minimum temperature for a room given its ID.'
        }
    ]
    
    return render_template('index.html', endpoints=endpoints)

@app.route('/<page_name>.html')
def static_page(page_name):
    return render_template(f'{page_name}.html')


def connect_and_query(query, the_fields):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()

        result_list = []
        for r in results:
            r_data = {}
            for f,d in zip(the_fields, r):
                r_data[f] = d
            result_list.append(r_data)

        response = make_response(jsonify(result_list))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    except Exception as e:
        error_message = f'Error when connecting with the database: {str(e)}'
        return jsonify({"error": error_message}), 500  # Devolver código 500 en caso de error

    finally:
        # Cerrar el cursor y la conexión solo si fueron inicializados
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/get_avg_temp_of_all_rooms', methods=['GET'])
def get_avg_temp_of_all_rooms():
    the_query = "SELECT AVG(temperature) as avg_temp FROM temperatures;"
    the_fields = ["avg_temp"]
    return connect_and_query(the_query, the_fields)


@app.route('/get_avg_temp_by_rooms', methods=['GET'])
def get_avg_temp_by_rooms():
    the_query = "SELECT rooms.id, rooms.name, AVG(temperature) as avg_temp \
                             FROM rooms INNER JOIN temperatures ON rooms.id = temperatures.room_id GROUP BY rooms.id, rooms.name ORDER BY rooms.id;"
    the_fields = ["room_id", "room_name", "avg_temp"]
    return connect_and_query(the_query, the_fields)


@app.route('/get_max_temp_by_rooms', methods=['GET'])
def get_max_temp_by_rooms():
    the_query = "SELECT rooms.id, rooms.name, MAX(temperature) as max_temp \
                             FROM rooms INNER JOIN temperatures ON rooms.id = temperatures.room_id GROUP BY rooms.id, rooms.name ORDER BY rooms.id;"
    the_fields = ["room_id", "room_name", "max_temp"]
    return connect_and_query(the_query, the_fields)


@app.route('/get_room_name_from_id/<int:room_id>', methods=['GET'])
def get_room_name_from_id(room_id):
    the_query = f"SELECT rooms.name FROM rooms WHERE id = {room_id};"
    the_fields = ["room_name"]
    return connect_and_query(the_query, the_fields)


@app.route('/get_room_avg_temp_from_id/<int:room_id>', methods=['GET'])
def get_room_avg_temp_from_id(room_id):
    the_query = f"SELECT AVG(temperature) as avg_temp FROM temperatures WHERE id = {room_id};"
    the_fields = ["avg_temp"]
    return connect_and_query(the_query, the_fields)

@app.route('/get_room_min_temp_from_id/<int:room_id>', methods=['GET'])
def get_room_min_temp_from_id(room_id):
    the_query = f"SELECT MIN(temperature) as min_temp FROM temperatures WHERE id = {room_id};"
    the_fields = ["min_temp"]
    return connect_and_query(the_query, the_fields)