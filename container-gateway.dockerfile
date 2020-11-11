FROM sbhdhr/ubuntu-python


COPY gateway.py /gateway.py
COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "./gateway.py" ]