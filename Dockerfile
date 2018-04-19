FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP ./app.py
EXPOSE 5000

COPY app.py app.py

ENV GUNICORN_WORKERS=5
ENV GUNICORN_BIND=0.0.0.0:5000

RUN echo "#!/bin/bash \n gunicorn --workers=${GUNICORN_WORKERS} --bind=${GUNICORN_BIND} app:app" > ./entrypoint.sh && \
  chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
