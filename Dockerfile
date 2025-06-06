FROM python:3.13-slim

COPY . /video_app

WORKDIR /video_app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y bash
# 声明容器内的端口
EXPOSE 5000
    
CMD ["python", "main_flask.py"]