FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY /services/user_service/ /app/services/user_service/
COPY /services/database.py /app/services/database.py

EXPOSE 8000

CMD ["uvicorn", "services.user_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
