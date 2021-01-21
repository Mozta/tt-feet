# app.py
# Required Imports
import os
import logging
import random
from deteccion import det
from deteccionfuzzy import dfuzzy
from apiexcel import send_fuzzy
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')
tt_ref = db.collection('TTInsole')
msj_ref = db.collection('messages')
log_ref = db.collection('logs')
der2_ref = db.collection('N3qGDjBhGXutx2fQ')
izq2_ref = db.collection('WLeKk038iX000kGz')

rand_init = random.SystemRandom ()

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        #### ----------- Obten num_serie y usurio vinculado ----------- #####
        num_serie = request.json['ns']
        userid = tt_ref.document("micros/ns/"+num_serie).collections()
        uid = list(userid)[0].id

        #### ----------- Obten variables nuevas del pie ----------- #####
        press_new = request.json['press']

        if int(num_serie[2]) % 2 != 0:
            #impar
            temp_new = der2_ref.document("testd/der/temp").get()
            temp_new = temp_new.to_dict()
            temp_new = temp_new['tder']
            
            hum_new = der2_ref.document("testd/der/hum").get()
            hum_new = hum_new.to_dict()
            hum_new = hum_new['hder']
          
        else:
            temp_new = izq2_ref.document("testi/izq/temp").get()
            temp_new = temp_new.to_dict()
            temp_new = temp_new['tizq']
            
            hum_new = izq2_ref.document("testi/izq/hum").get()
            hum_new = hum_new.to_dict()
            hum_new = hum_new['hizq']

        #### ----------- Obten variables pasadas del mismo pie ----------- #####
        temp_old = tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/temp").get()
        press_old = tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/press").get()
        hum_old = tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/hum").get()

        temp_old = temp_old.to_dict()
        press_old = press_old.to_dict()
        hum_old = hum_old.to_dict()

        if int(num_serie[2]) % 2 != 0:
            temp_old = temp_old['tder']
            press_old = press_old['pder']
            hum_old = hum_old['hder']
        else:
            temp_old = temp_old['tizq']
            press_old = press_old['piz']
            hum_old = hum_old['hizq']

        #### ----------- Obten variables pasadas contralaterales ----------- #####
        if int(num_serie[2]) % 2 != 0:
            ns_cont = "mc" + str(int(num_serie[2])+1)
        else:
            ns_cont = "mc" + str(int(num_serie[2])-1)

        temp_con = tt_ref.document("micros/ns/"+ns_cont+"/"+uid+"/temp").get()
        hum_con = tt_ref.document("micros/ns/"+ns_cont+"/"+uid+"/hum").get()

        temp_con = temp_con.to_dict()
        hum_con = hum_con.to_dict()

        if int(num_serie[2]) % 2 != 0:
            temp_con = temp_con['tizq']
            hum_con = hum_con['hizq']
        else:
            temp_con = temp_con['tder']
            hum_con = hum_con['hder']
            
        #### ----------- Entrada a función de detección fuzzy----------- #####
        [code_msj,nivel_riesgo,var1,var2,var3,var4] = dfuzzy(num_serie,press_old,temp_old,hum_old,press_new,temp_new,hum_new,temp_con,hum_con)
        print(code_msj,nivel_riesgo,var1,var2,var3,var4)
        send_fuzzy(code_msj,nivel_riesgo,var1,var2,var3,var4)
        if code_msj != 27:
            detect_alert(code_msj,uid)

        #### ----------- Promedio general de variables ----------- #####
        if nivel_riesgo == 0:
            if int(num_serie[2]) % 2 != 0:
                suma = 0
                for i in temp_new:
                    suma = suma + i
                prom_temp = round((suma / len(temp_new)),1)
                prom_hum = round(((hum_new[0] + hum_new[1]) / 2),1)
                gral = [prom_temp,prom_hum,85]
                prom_gral(num_serie,gral,uid)
        
        #### ----------- Establecer data en el usuario ----------- #####
        if nivel_riesgo == 0:
            if int(num_serie[2]) % 2 != 0:
                #IMPAR
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/hum").update({'hder':hum_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/temp").update({'tder':temp_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/press").update({'pder':request.json['press']})

                #2.0
                temperatura = [20,20,20,20,20,20,20]
                humedad = [70,70]

                for i in range(len(temperatura)):
                    temperatura[i] = round((temperatura[i] + rand_init.uniform (0.1, 0.5)),1)
                for i in range(2):
                    humedad[i] = round(humedad[i] +2 - rand_init.uniform (0, 2))

                der2_ref.document("testd/der/hum").update({'hder':humedad})
                der2_ref.document("testd/der/temp").update({'tder':temperatura})

            else:
                #PAR
                suma = 0
                for i in temp_new:
                    suma = suma + i
                prom_temp = round((suma / len(temp_new)),1)
                prom_hum = round(((hum_new[0] + hum_new[1]) / 2),1)

                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/gral").update({'batt':85, 'humg':prom_hum, 'tempg':prom_temp})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/hum").update({'hizq':hum_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/temp").update({'tizq':temp_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/press").update({'piz':request.json['press']})


            #2.0
                temperatura = [20,20,20,20,20,20,20]
                humedad = [70,70]

                for i in range(len(temperatura)):
                    temperatura[i] = round((temperatura[i] + rand_init.uniform (0.1, 0.5)),1)
                for i in range(2):
                    humedad[i] = round(humedad[i] +2 - rand_init.uniform (0, 2))

                izq2_ref.document("testi/izq/hum").update({'hizq':humedad})
                izq2_ref.document("testi/izq/temp").update({'tizq':temperatura})

        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/addn', methods=['POST'])
def crear():
    try:
        #### ----------- Obten num_serie y usurio vinculado ----------- #####
        num_serie = request.json['ns']
        userid = tt_ref.document("micros/ns/"+num_serie).collections()
        uid = list(userid)[0].id

        #### ----------- Obten variables nuevas del pie ----------- #####
        press_new = request.json['press']

        if int(num_serie[2]) % 2 != 0:
            #impar
            temp_new = der2_ref.document("testd/der/temp").get()
            temp_new = temp_new.to_dict()
            temp_new = temp_new['tder']
            
            hum_new = der2_ref.document("testd/der/hum").get()
            hum_new = hum_new.to_dict()
            hum_new = hum_new['hder']
          
        else:
            temp_new = izq2_ref.document("testi/izq/temp").get()
            temp_new = temp_new.to_dict()
            temp_new = temp_new['tizq']
            
            hum_new = izq2_ref.document("testi/izq/hum").get()
            hum_new = hum_new.to_dict()
            hum_new = hum_new['hizq']

        #### ----------- Obten variables pasadas del mismo pie ----------- #####
        temp_old = tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/temp").get()
        press_old = tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/press").get()
        hum_old = tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/hum").get()

        temp_old = temp_old.to_dict()
        press_old = press_old.to_dict()
        hum_old = hum_old.to_dict()

        if int(num_serie[2]) % 2 != 0:
            temp_old = temp_old['tder']
            press_old = press_old['pder']
            hum_old = hum_old['hder']
        else:
            temp_old = temp_old['tizq']
            press_old = press_old['piz']
            hum_old = hum_old['hizq']

        #### ----------- Obten variables pasadas contralaterales ----------- #####
        if int(num_serie[2]) % 2 != 0:
            ns_cont = "mc" + str(int(num_serie[2])+1)
        else:
            ns_cont = "mc" + str(int(num_serie[2])-1)

        temp_con = tt_ref.document("micros/ns/"+ns_cont+"/"+uid+"/temp").get()
        hum_con = tt_ref.document("micros/ns/"+ns_cont+"/"+uid+"/hum").get()

        temp_con = temp_con.to_dict()
        hum_con = hum_con.to_dict()

        if int(num_serie[2]) % 2 != 0:
            temp_con = temp_con['tizq']
            hum_con = hum_con['hizq']
        else:
            temp_con = temp_con['tder']
            hum_con = hum_con['hder']
            
        #### ----------- Entrada a función de detección ----------- #####
        [code_msj,nivel_riesgo] = det(num_serie,press_old,temp_old,hum_old,press_new,temp_new,hum_new,temp_con,hum_con)
        print(code_msj,nivel_riesgo)
        if code_msj != 27:
            detect_alert(code_msj,uid)

        #### ----------- Promedio general de variables ----------- #####
        if nivel_riesgo == 0:
            if int(num_serie[2]) % 2 != 0:
                suma = 0
                for i in temp_new:
                    suma = suma + i
                prom_temp = round((suma / len(temp_new)),1)
                prom_hum = round(((hum_new[0] + hum_new[1]) / 2))
                gral = [prom_temp,prom_hum,85]
                prom_gral(num_serie,gral,uid)
        
        #### ----------- Establecer data en el usuario ----------- #####
        if nivel_riesgo == 0:
            if int(num_serie[2]) % 2 != 0:
                #IMPAR
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/hum").update({'hder':hum_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/temp").update({'tder':temp_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/press").update({'pder':request.json['press']})

                #2.0
                temperatura = [20,20,20,20,20,20,20]
                humedad = [70,70]

                for i in range(len(temperatura)):
                    temperatura[i] = round((temperatura[i] + rand_init.uniform (0.1, 0.5)),1)
                for i in range(2):
                    humedad[i] = round(humedad[i] +2 - rand_init.uniform (0, 2))

                der2_ref.document("testd/der/hum").update({'hder':humedad})
                der2_ref.document("testd/der/temp").update({'tder':temperatura})

            else:
                #PAR
                suma = 0
                for i in temp_new:
                    suma = suma + i
                prom_temp = round((suma / len(temp_new)),1)
                prom_hum = round(((hum_new[0] + hum_new[1]) / 2),1)

                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/gral").update({'batt':85, 'humg':prom_hum, 'tempg':prom_temp})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/hum").update({'hizq':hum_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/temp").update({'tizq':temp_new})
                tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/press").update({'piz':request.json['press']})


            #2.0
                temperatura = [20,20,20,20,20,20,20]
                humedad = [70,70]

                for i in range(len(temperatura)):
                    temperatura[i] = round((temperatura[i] + rand_init.uniform (0.1, 0.5)),1)
                for i in range(2):
                    humedad[i] = round(humedad[i] +2 - rand_init.uniform (0, 2))

                izq2_ref.document("testi/izq/hum").update({'hizq':humedad})
                izq2_ref.document("testi/izq/temp").update({'tizq':temperatura})

        log_ref.document("testing").update({'cmsj': [code_msj,nivel_riesgo]})
        #print("holi")
        return jsonify({"success": True, 'cmsj': [code_msj,nivel_riesgo]}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')    
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200  
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/listn', methods=['GET'])
def lee():
    try:
        # Check if ID was passed to URL query

        #### ----------- Obten variables pasadas del mismo pie ----------- #####
        temp_der = tt_ref.document('micros/ns/mc1/IhvATIUo5tRBhadQgH84ngOWaT82/temp').get()
        press_der = tt_ref.document('micros/ns/mc1/IhvATIUo5tRBhadQgH84ngOWaT82/press').get()
        hum_der = tt_ref.document('micros/ns/mc1/IhvATIUo5tRBhadQgH84ngOWaT82/hum').get()

        temp_der = temp_der.to_dict()
        press_der = press_der.to_dict()
        hum_der = hum_der.to_dict()

        temp_der = temp_der['tder']
        hum_der = hum_der['hder']
        press_der = press_der['pder']


        #### ----------- Obten variables pasadas contralaterales ----------- #####
        temp_der_con = tt_ref.document('micros/ns/mc2/IhvATIUo5tRBhadQgH84ngOWaT82/temp').get()
        hum_der_con = tt_ref.document('micros/ns/mc2/IhvATIUo5tRBhadQgH84ngOWaT82/hum').get()

        temp_der_con = temp_der_con.to_dict()
        hum_der_con = hum_der_con.to_dict()

        temp_der_con = temp_der_con['tder']
        hum_der_con = hum_der_con['hder']

        


        #print(temp_der['tder'])
        return jsonify(temp_der), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


#### ----------- Función Promedio general de variables ----------- #####
def prom_gral(num_serie,gral,uid):
    num_serie2 = "mc" + str(int(num_serie[2])+1)
    gral2 = [0,0,0]
    info_gral = [0,0,0]
    #gral = request.json['gral']
    ctrltral = tt_ref.document("micros/ns/"+num_serie2+"/"+uid+"/gral").get()
    ctrltral = ctrltral.to_dict()
    gral2[0] = ctrltral['batt']
    gral2[1] = ctrltral['humg']
    gral2[2] = ctrltral['tempg']

    info_gral[0] = round((gral[2] + gral2[0]) / 2)
    info_gral[1] = round((gral[1] + gral2[1]) / 2)
    info_gral[2] = round(((gral[0] + gral2[2]) / 2),1)
    tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/gral").update({'batt':info_gral[0], 'humg':info_gral[1], 'tempg':info_gral[2]})


#### ----------- Función notificación de alerta ----------- #####
def detect_alert(arg, uid):
    #muid = str(randint(1, 1000))
    muid = "1111"
    msj_ref.document("msj"+muid).set({'cmsj': arg, 'userUid': uid})
        


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)