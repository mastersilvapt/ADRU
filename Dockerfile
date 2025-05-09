FROM python:3.11.2

COPY app /app

WORKDIR /app

RUN pip install -r requirements.txt

COPY .env /app/.env

CMD ["python", "main.py"]