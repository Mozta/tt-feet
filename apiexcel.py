import requests

def send_fuzzy(v1,v2,v3,v4,v5,v6):
    api_key = 'iwRSqqUFlg_kRYXsV4WbMrmsyWbJMDaQ1gK-A2-cJMJ'

    sensor_read = {'value1':str(v1)+","+str(v2)+","+str(v3)+","+str(v4)+","+str(v5)+","+str(v6)}
    request_headers = {'Content-Type': 'application/json'}
    request = requests.post(
    'http://maker.ifttt.com/trigger/detfuzzy/with/key/' + api_key,
    json=sensor_read,
    headers=request_headers)
    print(request.text)
    request.close()