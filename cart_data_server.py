import flask
from flask import request
import json
import time
from threading import Thread 


app = flask.Flask(__name__)
app.config["DEBUG"] = True


data={}

def refresh_data():
    global data
    
    with open('cart-data.json','r') as file:
        data = json.load(file) 
   
        
def flush_data():
    global data
    
    with open('cart-data.json', 'w') as fp:
        json.dump(data, fp,indent = 4, sort_keys=True)
        
        
def refresh_thread(n): 
    refresh_data()
    time.sleep(n) 


@app.route('/getallcarts', methods=['GET'])
def getall():
    return json.dumps(data,indent = 4, sort_keys=True)


@app.route('/getcartfor', methods=['GET'])
def get_prod():
    k=request.args['id']
    return str(data[k])


@app.route('/additem', methods=['POST'])
def add():
     uid=request.args['id']
     k=request.args['item']
     v=request.args['quant']
     if uid in data.keys():
         data[uid]=data[uid].update({k:int(v)}) 
     else:
         data[uid]={k:int(v)}
     flush_data()
     return "true"
     
@app.route('/updateitem', methods=['PUT'])
def update():
     uid=request.args['id']
     k=request.args['item']
     v=request.args['quant']
     if uid in data.keys():
         cartdic = data[uid]
         if k in cartdic.keys():
            cartdic[k]=int(v)
            flush_data()
            return "true"
         else:
            return "false"
           
     else:
       return "false"
   
@app.route('/deleteitem', methods=['DELETE'])
def delete():
     uid=request.args['id']
     k=request.args['item']
     if uid in data.keys():
         cartdic = data[uid]
         if k in cartdic.keys():
            cartdic.pop(k) 
            flush_data()
            return "true"
         else:
            return "false"
     else:
       return "false"
    


# t = Thread(target = refresh_thread, args =(10, )) 
# t.start() 

refresh_data()
app.run(host= '0.0.0.0', port=4001)
    
