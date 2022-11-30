FROM debian:buster
LABEL maintainer="dbrawand@nhs.net"
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install less make wget vim curl python3-dev python3-pip zlib1g-dev libbz2-dev liblzma-dev
RUN mkdir /logs
WORKDIR /app
COPY requirements.txt .
RUN pip3 install cython
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 3003
CMD ["gunicorn","app:app"]
