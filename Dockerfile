FROM ubuntu
RUN ls
RUN apt update
RUN apt install python3-pip -y
RUN dpkg --configure -a && apt install -y python3
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y pkg-config libmariadb-dev build-essential
RUN pip3 install -r requirement.txt
CMD ["python3","-m","flask","run","--host=0.0.0.0"]