FROM sbhdhr/ubuntu-python


COPY client1/* /

CMD [ "python3", "./rest_client_modified.py" ]

