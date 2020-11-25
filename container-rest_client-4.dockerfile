FROM sbhdhr/ubuntu-python


COPY client4/* /

CMD [ "python3", "./rest_client_modified.py" ]