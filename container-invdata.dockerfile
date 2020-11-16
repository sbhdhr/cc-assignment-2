FROM sbhdhr/ubuntu-python


COPY inv/inv-data.json /inv-data.json
COPY inv/inv_data_server.py /inv_data_server.py
COPY inv/create-inv-data.py /create-inv-data.py
COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "./inv_data_server.py" ]

