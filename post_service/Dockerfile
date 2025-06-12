# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Cài các package cần thiết
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Tạo thư mục làm việc
WORKDIR /app

# Copy file requirements và cài thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Expose port và chạy uvicorn
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
