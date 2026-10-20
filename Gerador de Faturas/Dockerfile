FROM python:3.12-slim

WORKDIR /app

COPY application/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY application/ .

EXPOSE 5000

CMD ["python3", "main.py"]
