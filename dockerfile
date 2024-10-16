From python:3.12-bullseye

ENV PYTHONBUFFERED=1

WORKDIR /EPL

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000

