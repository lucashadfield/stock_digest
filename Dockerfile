FROM python:3.11-slim
COPY . /stock_digest
WORKDIR /stock_digest
COPY email_secret.yaml /root/.config/stock_digest/email.yaml
COPY stocks_secret.yaml /root/.config/stock_digest/stocks.yaml

RUN pip3 install -r requirements.txt
RUN pip3 install .

CMD [ "stock_digest" ]