FROM python:3.13-slim
WORKDIR /app

RUN apt-get update && apt-get install -y ca-certificates

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
COPY requirements-docker.txt .
EXPOSE 8000

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu 

RUN pip install --no-cache-dir -r requirements-docker.txt
CMD ["python3", "src/gui.py"]