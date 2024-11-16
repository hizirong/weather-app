FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# 修改這裡，先更新 pip
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]