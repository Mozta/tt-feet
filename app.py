# app.py
# Required Imports
import os
from random import randint
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

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/addn', methods=['POST'])
def crear():
    try:
        #obtengo numserie y codigo de alerta
        num_serie = request.json['ns']
        code_msj = request.json['warn']
        #Consulta uid
        userid = tt_ref.document("micros/ns/"+num_serie).collections()
        uid = list(userid)[0].id
        #print(uid)
        print(request.json['warn'])
        #establecer data en el usuario
        #tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/hum").update({'hder':request.json['hder']})
        #tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/temp").update({'tder':request.json['tder']})
        tt_ref.document("micros/ns/"+num_serie+"/"+uid+"/press").set({'piz':request.json['piz']})
        #press = request.json['press']

        #print(request.json)
        #todo_ref.document('1').collection('testing').document('press').set('press':)

        def detect_alert(arg, uid):
            muid = str(randint(1, 1000))
            msj_ref.document("msj"+muid).set({'cmsj': arg, 'userUid': uid})

        if code_msj != 0:
            detect_alert(code_msj,uid)
        

        return jsonify({"success": True}), 200
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
        #todo_id = todo_ref.document('1').get()
        todo_id = todo_ref.document('1').collection('testing').get()
        #resultado = u'Document data: {}'.format(todo_id.to_dict())
        return jsonify(todo_id.to_dict()), 200
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
        
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)