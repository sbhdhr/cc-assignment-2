import flask
from flask import request
import json
from kazoo.client import KazooClient
import socket 
import time
import requests
import logging


app = flask.Flask(__name__)

app.debug = True
app.logger.setLevel(logging.DEBUG)

host_name = socket.gethostname()


LOCAL_FLAG = False


if LOCAL_FLAG:
    invdata = ["http://localhost:3001","http://localhost:3002"]
    cartdata = ["http://localhost:4001","http://localhost:4002"]
    
    zk = KazooClient(hosts='localhost:2181')
    zk.start()
    lock = zk.Lock("/lockpath/inv", "1234")
    
else:
    invdata = ["http://invdata1:3000","http://invdata2:3000"]
    cartdata = ["http://cartdata1:4000","http://cartdata2:4000"]
    zk = KazooClient(hosts='zoo1:2181')
    zk.start()
    lock = zk.Lock("/lockpath/inv", "1234")


invlock=["inv1","inv2"]
cartlock=["cart1","cart2"]

@app.route('/testaq', methods=['GET'])
def testaq():
    while True:
        lock = zk.WriteLock("/lockpath/inv", "1234")
        with lock:  # blocks waiting for lock acquisition
            print(host_name,":: Lock acquired..")
            print(host_name,":: Processing..")
            time.sleep(2)
            print(host_name,":: Lock released..")


@app.route('/testlog', methods=['GET'])
def testlog():
    app.logger.error("A warning")
    return ""

@app.route('/getallcarts', methods=['GET'])
def getall():
    uid=request.args['id']
    passwrd=request.args['pass']
    
    if uid=='0' and passwrd=='pass':
        try:
            data = {}
            for i,url in enumerate(cartdata):
                lock = zk.WriteLock("/lockpath/"+cartlock[i], cartlock[i])
                with lock:
                    cartdict = requests.get(url+"/getallcarts").json()
                    data.update(cartdict)
                    app.logger.info(str(data))
                #data.update()
            return json.dumps(data,indent = 4, sort_keys=True)
        except Exception as e:
            return str(e)
    else:
        return "false"
    
@app.route('/listallitems', methods=['GET'])
def listallitems():
    try:
        data = []
        for i,url in enumerate(invdata):
            lock = zk.WriteLock("/lockpath/"+invlock[i], invlock[i])
            with lock:
                invdict = requests.get(url+"/getall").json()
                tmp=[]
                for k in invdict.keys():
                    tmp.append((k,invdict[k]['quan']))
                data = data+tmp
                app.logger.info(str(data))
            #data.update()
        return json.dumps(data,indent = 4, sort_keys=True)
    except Exception as e:
        return str(e)


     
@app.route('/getcartfor', methods=['GET'])
def get_cart_for():
    k=request.args['id']
    part=int(request.args['part'])
    try:
        lock = zk.WriteLock("/lockpath/"+cartlock[part], cartlock[part])
        with lock:
            cartdict = requests.get(cartdata[part]+"/getcartfor",params={'id':k}).json()
            app.logger.info(str(cartdict))
            return json.dumps(cartdict,indent = 4, sort_keys=True)
    except Exception as e:
        return str(e)
    
    
@app.route('/additem', methods=['POST'])
def add():
     uid=request.args['id']
     k=request.args['item']
     v=request.args['quant']
     invpart=int(request.args['invpart'])
     cartpart=int(request.args['cartpart'])
     try:
        #decrease inv for item. if successful, add in cart
        lock = zk.WriteLock("/lockpath/"+invlock[invpart], invlock[invpart])
        with lock:
            invres = requests.post(invdata[invpart]+"/decquan",params={'key':k,'val':v}).text
            if invres=='true':
                lock2 = zk.WriteLock("/lockpath/"+cartlock[cartpart], cartlock[cartpart])
                with lock2:
                    res = requests.post(cartdata[cartpart]+"/additem",params={'id':uid,'item':k,'quant':v}).text
                    app.logger.info(res)
                    return res
            else:
                return 'false'
     except Exception as e:
        return str(e) 

@app.route('/updateitem', methods=['PUT'])
def updateitem():
     uid=request.args['id']
     k=request.args['item']
     v=int(request.args['quant'])
     invpart=int(request.args['invpart'])
     cartpart=int(request.args['cartpart'])
     
     try:
        lock = zk.WriteLock("/lockpath/"+invlock[invpart], invlock[invpart])
        with lock:
            invres = requests.get(invdata[invpart]+"/getprodquan",params={'key':k}).text
            if v>=1 and v<=int(invres):
                lock2 = zk.WriteLock("/lockpath/"+cartlock[cartpart], cartlock[cartpart])
                with lock2:
                        cartres = requests.get(cartdata[cartpart]+"/getcartquanfor",params={'id':uid,'item':k}).text
                        cartres = int(cartres)
                        invres = requests.post(invdata[invpart]+"/incquan",params={'key':k,'val':cartres}).text
                        invres = requests.post(invdata[invpart]+"/decquan",params={'key':k,'val':v}).text
                        res = requests.put(cartdata[cartpart]+"/updateitem",params={'id':uid,'item':k,'quant':v}).text
                        app.logger.info(res)
                        return 'true'
            else:
                return 'false'
     except Exception as e:
        return str(e) 
    
@app.route('/deleteitem', methods=['DELETE'])
def deleteitem():
     uid=request.args['id']
     k=request.args['item']
     invpart=int(request.args['invpart'])
     cartpart=int(request.args['cartpart'])
     try:
         lock2 = zk.WriteLock("/lockpath/"+cartlock[cartpart], cartlock[cartpart])
         with lock2:
             cartres = requests.get(cartdata[cartpart]+"/getcartquanfor",params={'id':uid,'item':k}).text
             cartres = int(cartres)
             if cartres != -1:
                   cartres2 = requests.delete(cartdata[cartpart]+"/deleteitem",params={'id':uid,'item':k}).text
                   if cartres2 == "true":
                        
                        lock = zk.WriteLock("/lockpath/"+invlock[invpart], invlock[invpart])
                        with lock:
                            invres = requests.post(invdata[invpart]+"/incquan",params={'key':k,'val':cartres}).text
                            #app.logger.info("invres: "+invres)
                            if invres=="true":
                                return 'true'
                            else:
                                return 'false'
                   else:
                    return 'false'  
             else:
                 return 'false'           
     except Exception as e:
        return str(e) 

app.run(host= '0.0.0.0', port=5000)