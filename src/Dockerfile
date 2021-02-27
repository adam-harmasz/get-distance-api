FROM python:3.8.2
ENV PYTHONUNBUFFERED=1 \
	DOCKERIZE_VERSION=v0.6.1

# Installing `dockerize` utility:
# https://github.com/jwilder/dockerize
RUN wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
&& tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
&& rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" && dockerize --version

WORKDIR /src

COPY requirements.txt /src/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /src/
