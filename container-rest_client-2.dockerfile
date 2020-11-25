FROM sbhdhr/ubuntu-python


COPY client2/* /

CMD [ "python3", "./rest_client_modified.py" ]

