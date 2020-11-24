FROM sbhdhr/ubuntu-python


COPY inv1/* /
COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "./inv_data_server.py" ]