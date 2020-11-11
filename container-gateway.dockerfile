FROM sbhdhr/ubuntu-python


COPY gateway.py /gateway.py

CMD [ "python3", "./gateway.py" ]