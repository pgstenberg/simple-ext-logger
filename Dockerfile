FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP ./app.py
EXPOSE 5000

COPY app.py app.py

ENTRYPOINT flask run --host=0.0.0.0
