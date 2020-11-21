from flask import Flask
from flask import request
from kazoo.client import KazooClient
import socket 
import requests
import logging


app = Flask(__name__)

app.debug = True
app.logger.setLevel(logging.DEBUG)

host_name = socket.gethostname()


LOCAL_FLAG = True


if LOCAL_FLAG:
    restsrv = ["http://localhost:5001","http://localhost:5002"]
    
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    lock = zk.Lock("/lockpath/inv", "1234")
    
else:
    restsrv = ["http://restsrv1:5000","http://restsrv2:5000"]
    
    zk = KazooClient(hosts='zoo1:2181')
    zk.start()
    lock = zk.Lock("/lockpath/inv", "1234")

@app.route('/testlog', methods=['GET'])
def testlog():
    app.logger.error("A warning")
    return ""


part=1

def find_part_for_user_cart(id):
    #crush code
    map1 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
    return map1[id]

def find_part_for_inv(item):
    #crush code
    
    return 1

@app.route('/getallcarts', methods=['GET'])
def getall():
    uid=request.args['id']
    passwrd=request.args['pass']
    
    part = find_part_for_user_cart(int(uid))
    
    try:
        res = requests.get(restsrv[part]+"/getallcarts",params={'id':uid,'pass':passwrd}).text
        return res
    except Exception as e:
       return str(e)
   
    
@app.route('/listallitems', methods=['GET'])
def listallitems():
     uid=request.args['id']
     
     part = find_part_for_user_cart(int(uid))
    
     try:
        res = requests.get(restsrv[part]+"/listallitems").text
        return res
     except Exception as e:
       return str(e)


     
@app.route('/getcartfor', methods=['GET'])
def get_cart_for():
     uid=request.args['id']
     
     part = find_part_for_user_cart(int(uid))
    
     try:
        res = requests.get(restsrv[part]+"/getcartfor",params={'id':uid,'part':part}).text
        return res
     except Exception as e:
       return str(e)
    
    
@app.route('/additem', methods=['POST'])
def add():
     uid=request.args['id']
     k=request.args['item']
     v=request.args['quant']
     
     invpart = find_part_for_inv(k)
     cartpart = find_part_for_user_cart(int(uid))

    
     try:
        res = requests.post(restsrv[part]+"/additem",params={'id':uid,
                                                            'item':k,
                                                            'quant':v,
                                                            'invpart':invpart,
                                                            'cartpart':cartpart}).text
        return res
     except Exception as e:
       return str(e)

@app.route('/updateitem', methods=['PUT'])
def updateitem():
     uid=request.args['id']
     k=request.args['item']
     v=request.args['quant']
     
     invpart = find_part_for_inv(k)
     cartpart = find_part_for_user_cart(int(uid))

    
     try:
        res = requests.put(restsrv[part]+"/updateitem",params={'id':uid,
                                                            'item':k,
                                                            'quant':v,
                                                            'invpart':invpart,
                                                            'cartpart':cartpart}).text
        return res
     except Exception as e:
       return str(e) 
    
@app.route('/deleteitem', methods=['DELETE'])
def deleteitem():
     uid=request.args['id']
     k=request.args['item']
     
     invpart = find_part_for_inv(k)
     cartpart = find_part_for_user_cart(int(uid))

    
     try:
        res = requests.delete(restsrv[part]+"/deleteitem",params={'id':uid,
                                                            'item':k,
                                                            'invpart':invpart,
                                                            'cartpart':cartpart}).text
        return res
     except Exception as e:
       return str(e) 

app.run(host= '0.0.0.0', port=6000)