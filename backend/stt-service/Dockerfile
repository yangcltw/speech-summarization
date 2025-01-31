FROM python:3.11-slim

# 安裝 GNU OpenMP
RUN apt-get update && apt-get install -y libgomp1

# on Ubuntu or Debian
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "stt-service:app", "--host", "0.0.0.0", "--port", "8000"]
