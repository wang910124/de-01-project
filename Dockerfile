FROM python:3.12-slim

WORKDIR /app

COPY test_api.py /app/test_api.py

RUN mkdir -p /app/data

CMD ["python", "test_api.py"]
