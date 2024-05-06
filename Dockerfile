FROM python:3.8.2

ENV FLASK_APP=app \
    HOME=/root \
    FLASK_RUN_HOST=0.0.0.0

WORKDIR /root

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

RUN apt-get update && apt-get install -y curl \
    && curl -L https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait -o /wait \
    && chmod +x /wait

RUN chmod +x /wait

CMD /wait && python -u server.py
