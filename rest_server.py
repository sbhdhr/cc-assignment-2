# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:08:45 2020

@author: Subhashis
"""

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True



books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/apiv1/test', methods=['GET'])
def test():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/apiv1/inventory/all', methods=['GET'])
def get_all_inv():
    return jsonify(books)




app.run(host= '0.0.0.0')