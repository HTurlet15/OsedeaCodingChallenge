FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir numpy opencv-python-headless matplotlib

CMD ["python3", "./main.py"]
