import flask
from flask import request
import json


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
        

@app.route('/getallcarts', methods=['GET'])
def getall():
    return json.dumps(data,indent = 4, sort_keys=True)


@app.route('/getcartfor', methods=['GET'])
def get_cart_for():
    k=request.args['id']
    if k in data.keys():
        return json.dumps(data[k],indent = 4, sort_keys=True)
    else:
        return json.dumps({},indent = 4, sort_keys=True)
    
@app.route('/getcartquanfor', methods=['GET'])
def getcartquanfor():
    k=request.args['id']
    item=request.args['item']
    if k in data.keys():
        return str(data[k][item])
    else:
        return str(-1)



@app.route('/additem', methods=['POST'])
def add():
     uid=request.args['id']
     k=request.args['item']
     v=request.args['quant']
     if uid in data.keys():
         cartdic = data[uid]
         if k not in cartdic.keys():
             cartdic.update({k:int(v)})
             flush_data()
             return "true"
         else:
             return "false"
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
   
@app.route('/deletecart', methods=['DELETE'])
def delete_cart():
     uid=request.args['id']
     if uid in data.keys():
        data.pop(uid) 
        flush_data()
        return "true"
     else:
       return "false"
    


# t = Thread(target = refresh_thread, args =(10, )) 
# t.start() 

refresh_data()
app.run(host= '0.0.0.0', port=4000)
    
