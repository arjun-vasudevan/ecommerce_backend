FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY /services/cart_service/ /app/services/cart_service/
COPY /services/*.py /app/services/

EXPOSE 8000

CMD ["uvicorn", "services.cart_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
