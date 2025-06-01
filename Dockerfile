FROM docker.arvancloud.ir/tiangolo/uwsgi-nginx-flask

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt 
# RUN pip install debugpy
COPY . /app
EXPOSE 80
ENV SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:aaaa@localhost:5432/fitbook
COPY .env /app/.env
