# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default to production
ARG FLASK_ENV=production
ENV FLASK_ENV=${FLASK_ENV}
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["sh", "-c", "if [ '$FLASK_ENV' = 'development' ]; then flask run --host=0.0.0.0 --port=5000; else gunicorn -b 0.0.0.0:5000 app:app; fi"] 
