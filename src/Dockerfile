FROM python:3.8.2
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# Update system and install deps
RUN apt-get update \
    && apt-get install -yq \
    netcat \
    libpq-dev \
    build-essential \
    libmagic-dev

COPY requirements.txt /src/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /src/
