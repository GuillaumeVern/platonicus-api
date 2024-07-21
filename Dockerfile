FROM python:3.12-alpine

WORKDIR /

RUN pip install fastapi pydantic typing mysql-connector-python==8.3.0 passlib python-jose

RUN apk add git

RUN git clone https://github.com/GuillaumeVern/platonicus-api

WORKDIR platonicus-api

RUN git pull

EXPOSE 8000

CMD ["sh", "-c", "git pull; fastapi run main.py --port 8000"]
