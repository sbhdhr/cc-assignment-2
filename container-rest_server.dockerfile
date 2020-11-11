FROM sbhdhr/ubuntu-python


COPY rest_server.py /rest_server.py

CMD [ "python3", "./rest_server.py" ]