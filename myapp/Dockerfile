FROM python:3.8

RUN mkdir -p /myapp
WORKDIR /myapp

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /myapp

CMD flask run --host=0.0.0.0

