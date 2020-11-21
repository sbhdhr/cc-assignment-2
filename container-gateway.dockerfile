FROM sbhdhr/ubuntu-python2


COPY gateway/gateway.py /gateway.py
COPY requirements.txt /requirements.txt
#
RUN pip install -r requirements.txt
#
CMD [ "python", "./gateway.py" ]