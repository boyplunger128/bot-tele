FROM python:3.10.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

CMD python3 bot.py