FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

COPY main.py /app/main.py
COPY data /app/data

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

