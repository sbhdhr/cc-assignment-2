FROM sbhdhr/ubuntu-python


COPY client3/* /

CMD [ "python3", "./rest_client_modified.py" ]

