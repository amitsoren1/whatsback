FROM python:3.9.9-slim-buster
EXPOSE 80
COPY . /whatsapp/backend

WORKDIR /whatsapp/backend
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
