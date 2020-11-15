import flask
from flask import request
import json
from datetime import datetime
import time
from threading import Thread 


app = flask.Flask(__name__)
app.config["DEBUG"] = True


data={}

def refresh_data():
    global data
    
    with open('inv-data.json','r') as file:
        data = json.load(file) 
        
        
def flush_data():
    global data
    
    with open('inv-data.json', 'w') as fp:
        json.dump(data, fp,indent = 4, sort_keys=True)
        
        
def refresh_thread(n): 
    refresh_data()
    time.sleep(n) 


@app.route('/getall', methods=['GET'])
def getall():
    return json.dumps(data,indent = 4, sort_keys=True)


@app.route('/getprod', methods=['GET'])
def get_prod():
    k=request.args['key']
    return str(data[k])


@app.route('/update', methods=['POST'])
def update():
     k=request.args['key']
     v=request.args['val']
     if k in data.keys():
         data[k]=(int(v),datetime.timestamp(datetime.now()))
         flush_data()
         return "true"
     else:
         return "false"
    


t = Thread(target = refresh_thread, args =(10, )) 
t.start() 

refresh_data()
app.run(host= '0.0.0.0', port=3000)
    
