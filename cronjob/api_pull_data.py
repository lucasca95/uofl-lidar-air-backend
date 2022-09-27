import pdb
import json, os
import requests as rqs
import pymysql
from time import sleep


from dotenv import load_dotenv
load_dotenv()

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
#region   OAuth and Ubicquia
# =============================================================================
access_token_response = rqs.post(
                            os.getenv('UBIVU_TOKEN_URL'),
                            data={'grant_type': os.getenv('UBIVU_GRANT_TYPE')},
                            verify=False,
                            allow_redirects=False,
                            auth=(
                                os.getenv('UBIVU_CLIENTID'), 
                                os.getenv('UBIVU_KEY')
                            )
                        )
access_token = json.loads(access_token_response.text)
api_call_headers = {
    'Authorization': 'Bearer ' + access_token['access_token'],
    "accept": "application/json",
    "Content-Type": "application/json"
}
api_call_response = rqs.get(
    'https://api.ubicquia.com/api/nodes/2?type=aqi', 
    headers=api_call_headers, 
    verify=False
)
air_data = json.loads(api_call_response.text).get('data')
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
            air_data.get('pm1_0'), 
            air_data.get('pm2_5'), 
            air_data.get('pm10'), 
            air_data.get('co'), 
            air_data.get('temperature_f'), 
            air_data.get('pressure'), 
            air_data.get('humidity'), 
            air_data.get('noise_level'), 
            air_data.get('id')
            ]
        )
    connection.commit()
    # print(f"Air Sample added successfully!")

except Exception as ee:
    print(f"DB error: {ee}")
#endregion
