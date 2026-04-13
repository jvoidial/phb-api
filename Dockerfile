FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PHB_API_MODE=fastapi

CMD ["uvicorn", "phb_api:fastapi_app", "--host", "0.0.0.0", "--port", "8080"]
