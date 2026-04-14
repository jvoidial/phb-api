FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# force rebuild Tue Apr 14 15:08:21 BST 2026
# force rebuild Tue Apr 14 15:12:39 BST 2026
