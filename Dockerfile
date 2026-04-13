FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PHB_API_MODE=fastapi

CMD ["python3", "phb_api.py"]
