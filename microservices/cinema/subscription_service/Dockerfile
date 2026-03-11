FROM python:3.11-slim
WORKDIR /svc
COPY requirements.txt /svc/requirements.txt
RUN pip install --no-cache-dir -r /svc/requirements.txt
COPY microservices/cinema/subscription_service /svc/subscription_service
EXPOSE 8002
CMD ["uvicorn", "subscription_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
