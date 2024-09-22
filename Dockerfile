FROM python:3.11-slim
COPY . /stock_digest
WORKDIR /stock_digest

RUN pip3 install -r requirements.txt
RUN pip3 install .

CMD [ "stock_digest" ]
