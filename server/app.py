from http import client
import os
import pdb
from time import sleep
from unicodedata import name

from flask import Flask, request, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

import json
import requests as rqs

import pymysql

from dotenv import load_dotenv
load_dotenv()

# =============================================================================
#   Used to check the BASE_URL of the project
# =============================================================================
print(f"\nCheck value of BASE_URL: {os.getenv('BASE_URL')}\n")

# =============================================================================
#   Flask app declaration and config setup
# =============================================================================
app = Flask(__name__)
app.config["SECRET_KEY"] = 'jv5(78$62-hr+8==+kn4%r*(9g)fubx&&i=3ewc9p*tnkt6u$h'
# app.config["SERVER_NAME"] = 'add server name'
app.config["MAIL_SERVER"] = 'smtp.mail.yahoo.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

CORS(app, origins="*")
api = Api(app)


# =============================================================================
#region   Connection with DB
# =============================================================================
db_connected = False
while (not db_connected):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='PASSWORD',
            database='lge',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        db_connected=True
    except:
        print(f'\nError with db connection\n')
        sleep(2)
#endregion


# =============================================================================
#region   Route behaviors
# =============================================================================

# NOTE: Data values are not being validated
class ProcessNewData(Resource):
    def get(self):
        return {
            'status': 200,
            'message': 'Not valid method for this endpoint'
        }

    def post(self):
        try:
            device_id = request.json.get('id')
            if (not device_id):
                raise ValueError("Device id needed but not received")
        except Exception as ee:
            return {
                'status': 200,
                'message': f"{ee}"
            }

        lidar_data = request.json.get('lidar')
        air_data = request.json.get('air')
        message = ""

        if (lidar_data):
            try:
                with connection.cursor() as cursor:
                    sql = """
                        INSERT INTO LIDAR(
                            people,
                            vehicles,
                            device_id
                        )VALUES(
                            %s,
                            %s,
                            %s
                        )
                    """
                    cursor.execute(sql, [
                        lidar_data.get('people'), 
                        lidar_data.get('vehicles'), 
                        device_id
                        ]
                    )
                connection.commit()
                message += "LIDAR."

            except Exception as ee:
                print(f"DB error: {ee}")

        if (air_data):
            try:
                with connection.cursor() as cursor:
                    sql = """
                        INSERT INTO AIR(
                            so2,
                            aqi,
                            no2,
                            o3,
                            pm1p0,
                            pm2p5,
                            pm10,
                            co,
                            temp,
                            pres,
                            relhum,
                            noise,
                            device_id
                        )VALUES(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                    """
                    cursor.execute(sql, [
                        air_data.get('so2'), 
                        air_data.get('aqi'), 
                        air_data.get('no2'), 
                        air_data.get('o3'), 
                        air_data.get('pm1p0'), 
                        air_data.get('pm2p5'), 
                        air_data.get('pm10'), 
                        air_data.get('co'), 
                        air_data.get('temp'), 
                        air_data.get('pres'), 
                        air_data.get('relhum'), 
                        air_data.get('noise'), 
                        device_id
                        ]
                    )
                connection.commit()
                message += "AIR."
            except Exception as ee:
                print(f"DB error: {ee}")

        return {
            'status': 200,
            'message': message
        }
       
class GetLidarData(Resource):
    def get(self):
        return {
            'status': 200,
            'message': 'Not valid method for this endpoint'
        }

    def post(self):
        device_id = request.json.get("id")
        # pdb.set_trace(); print("")
        if not device_id:
            return {
                'status': 200,
                'message': "Expected id not found"
            }
        
        data = []

        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT ll.people, ll.vehicles, ll.timedate FROM `LIDAR` as ll
                    WHERE ll.device_id = %s
                    ORDER BY ll.timedate DESC
                    LIMIT 10
                """
                cursor.execute(sql, [device_id]
                )
                for elem in cursor:
                    data.append({
                        'people': elem['people'],
                        'vehicles': elem['vehicles'],
                        'datetime': str(elem['timedate'])
                    })

            connection.commit()

        except Exception as ee:
            print(f"DB error: {ee}")
            return {
                'status': 201,
                'message': 'Internal error'
            }

        return {
            'status': 200,
            'device_id': device_id,
            'data': data
        }

class GetAirData(Resource):
    def get(self):
        return {
            'status': 200,
            'message': 'Not valid method for this endpoint'
        }

    def post(self):
        sleep(1.2)
        device_id = request.json.get("id")
        
        if not device_id:
            return {
                'status': 200,
                'message': "Expected id not found"
            }
        
        data = []

        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT 
                        aa.aqi,
                        aa.so2,
                        aa.no2,
                        aa.o3,
                        aa.pm1p0,
                        aa.pm2p5,
                        aa.pm10,
                        aa.co,
                        aa.temp,
                        aa.pres,
                        aa.relhum,
                        aa.noise
                    FROM AIR as aa
                    WHERE aa.device_id = %s
                    ORDER BY timedate DESC
                    LIMIT 1;
                """
                cursor.execute(sql, [device_id]
                )
                for elem in cursor:
                    data.append({
                        'aqi': elem['aqi'],
                        'so2': elem['so2'],
                        'no2': elem['no2'],
                        'o3': elem['o3'],
                        'pm1p0': elem['pm1p0'],
                        'pm2p5': elem['pm2p5'],
                        'pm10': elem['pm10'],
                        'co': elem['co'],
                        'temp': elem['temp'],
                        'pres': elem['pres'],
                        'relhum': elem['relhum'],
                        'noise': elem['noise']
                    })
            sleep(1)
            connection.commit()

        except Exception as ee:
            print(f"DB error: {ee}")
            return {
                'status': 201,
                'message': 'Internal error'
            }
        
        return {
            'status': 200,
            'device_id': device_id,
            'data': data
        }


class Home(Resource):
    def get(self):

        return {
            'status': 200,
            'message': 'Server up and running!'
        }
#endregion


# =============================================================================
#region   Routes declaration
# =============================================================================
api.add_resource(ProcessNewData, '/newdata/')
api.add_resource(GetLidarData, '/get/lidar/')
api.add_resource(GetAirData, '/get/air/')
api.add_resource(Home, '/')
#endregion


# =============================================================================
#   Used to run flask server as python script
# =============================================================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")