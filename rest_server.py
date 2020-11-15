import flask
from flask import request
import json
from kazoo.client import KazooClient
import socket 
import time


app = flask.Flask(__name__)
app.config["DEBUG"] = True

host_name = socket.gethostname()

invdata1 = "http://invdata1:3000"
invdata2 = "http://invdata2:3000"

zk = KazooClient(hosts='zoo1:2181')
zk.start()
lock = zk.Lock("/lockpath/inv", "1234")


@app.route('/testaq', methods=['GET'])
def testaq():
    while True:
        lock = zk.WriteLock("/lockpath/inv", "1234")
        with lock:  # blocks waiting for lock acquisition
            print(host_name,":: Lock acquired..")
            print(host_name,":: Processing..")
            time.sleep(2)
            print(host_name,":: Lock released..")


app.run(host= '0.0.0.0', port=3001)