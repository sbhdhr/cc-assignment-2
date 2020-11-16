FROM sbhdhr/ubuntu-python

#COPY HelloKazoo.py /HelloKazoo.py
COPY rest/rest_server.py /rest_server.py
COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "./rest_server.py" ]