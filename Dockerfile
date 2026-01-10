FROM python:3.13-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
COPY requirements-docker.txt .
EXPOSE 12399

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu 

RUN pip install --no-cache-dir -r requirements-docker.txt
CMD ["flet", "run", "--web", "--port", "12399", "src/gui.py"]