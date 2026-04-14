FROM python:3.11-slim

WORKDIR /app

# Force fresh copy of the entire repo (no cache)
ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "phb_runtime.py"]
