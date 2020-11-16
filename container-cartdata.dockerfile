FROM sbhdhr/ubuntu-python


COPY cart/cart-data.json /cart-data.json
COPY cart/cart_data_server.py /cart_data_server.py
COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "./cart_data_server.py" ]

