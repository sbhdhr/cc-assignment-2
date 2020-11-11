import flask
from flask import request, jsonify
import json
from fabric.connection import Connection



app = flask.Flask(__name__)
app.config["DEBUG"] = True



with Connection("invdata1", "root") as c, c.sftp() as sftp, sftp.open('remote_filename') as file:
    data = json.load('inv-data.json') 


@app.route('/apiv1/test', methods=['GET'])
def test():
    return json.dumps(data,indent = 4, sort_keys=True)


@app.route('/apiv1/inventory/all', methods=['GET'])
def get_all_inv():
    return ""



app.run(host= '0.0.0.0', port=3001)