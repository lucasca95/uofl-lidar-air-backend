import os
import pdb
from time import sleep

from flask import Flask, request, send_file, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

import pymysql

from dotenv import load_dotenv
load_dotenv()

# =============================================================================
#   Used to check the BASE_URL of the project
# =============================================================================
print(f"\nCheck value of BASE_URL: {os.getenv('BASE_URL')}\n")

# =============================================================================
#   List of allowed file extensions
# =============================================================================
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'dcom'}

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
#   Connection with DB
# =============================================================================
db_connected = False
while (not db_connected):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='db_lidar_air',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        db_connected=True
    except:
        print(f'\nError with db connection\n')
        sleep(5)

# =============================================================================
#   Route behaviors
# =============================================================================

# NOTE: Data values are not being validated
class ProcessNewData(Resource):
    def get(self):
        return {
            'status': 200,
            'message': 'Not valid method for this endpoint'
        }
    
    def post(self):
        raspberry_id = request.json.get('id')
        raspberry_data = request.json.get('data')
        try:
            if raspberry_id and raspberry_data:
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
                        cursor.execute(sql, [raspberry_data.get('people'), raspberry_data.get('vehicles'), raspberry_id])
                    connection.commit()
                except Exception as e:
                    return {
                        'status': 404,
                        'message': f'DB error: {e}',
                    }
                return {
                    'status': 200,
                    'message': f'Data (people: {raspberry_data.get("people")}; vehicles: {raspberry_data.get("vehicles")}) accepted for device {raspberry_id}'
                }
            else:
                raise Exception("Incorrect parameter values for 'id' and 'data'")
        except Exception as e:
            return {
                'status': 404,
                'message': f'Server error: {e}'
            }
        
        

class Home(Resource):
    def get(self):
        return {
            'status': 200,
            'message': 'Server up and running!'
        }

# =============================================================================
#   Routes declaration
# =============================================================================
api.add_resource(ProcessNewData, '/newdata/')
api.add_resource(Home, '/')

# @app.route('/login/', methods=['POST'])
# def login():
#     # pdb.set_trace()
#     auth = request.authorization
#     print(request.authorization)
#     if auth and auth.password == 'password':
#         token = jwt.encode({
#             'user': auth.username,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
#         }, app.config['SECRET_KEY'])
#         return jsonify({'token': token.decode('UTF-8')})
#     return make_response('Could NOT verify user', 401, {'WWW_Authenticate':'Basic realm="Login Required"'})

# =============================================================================
#   Used to run flask server as python script
# =============================================================================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")