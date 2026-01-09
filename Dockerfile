FROM python:3.13-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu 

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# COPY ./assets ./assets
CMD ["flet", "run", "--web", "--port", "62399", "src/gui.py"]