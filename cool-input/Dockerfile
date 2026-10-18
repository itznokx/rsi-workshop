FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app.py ./
COPY backend/templates/ templates/
ENV APP_HOST=127.0.0.1
EXPOSE 5000
CMD ["python", "app.py"]
