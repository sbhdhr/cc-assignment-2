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
    
    with open('inv-data-1.json','r') as file:
        data = json.load(file) 
        
        
def flush_data():
    global data
    
    with open('inv-data-1.json', 'w') as fp:
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
    if k in data.keys():
        return json.dumps(data[k],indent = 4, sort_keys=True)
    else:
        return json.dumps({},indent = 4, sort_keys=True)
    
@app.route('/getprodquan', methods=['GET'])
def getprodquan():
    k=request.args['key']
    if k in data.keys():
        return str(data[k]['quan'])
    else:
        return str(-1)

@app.route('/upquan', methods=['PUT'])
def upquan():
     k=request.args['key']
     v=request.args['val']
     if k in data.keys():
        invdict = data[k]
        invdict['quan']=int(v)
        invdict['time']=datetime.timestamp(datetime.now())
        flush_data()
        return "true"
     else:
         return "false"

@app.route('/decquan', methods=['POST'])
def decquan():
     k=request.args['key']
     v=request.args['val']
     if k in data.keys():
         invdict = data[k]
         if invdict['quan']-int(v)>=0:
             invdict['quan']=invdict['quan']-int(v)
             invdict['time']=datetime.timestamp(datetime.now())
             flush_data()
             return "true"
         else:
             return "false"
     else:
         return "false"
     
@app.route('/incquan', methods=['POST'])
def incquan():
     k=request.args['key']
     v=request.args['val']
     if k in data.keys():
        invdict = data[k]
        invdict['quan']=invdict['quan']+int(v)
        invdict['time']=datetime.timestamp(datetime.now())
        flush_data()
        return "true"
     else:
         return "false"
    


t = Thread(target = refresh_thread, args =(10, )) 
t.start() 

refresh_data()
app.run(host= '0.0.0.0', port=3000)
    
