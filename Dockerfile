# FROM 192.168.128.156/k8s-public/ai/python:3.10-slim
FROM python:3.11.12-slim

# ocr需要更新包
# RUN apt-get update && apt-get install libgl1 -y

# 时区修正
RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

WORKDIR /app

# Copy Application
COPY . /app

COPY nltk_data /usr/local/share/nltk_data

ARG env
ENV envType $env

# Install Dependencies
RUN pip install --no-cache-dir -r requirements/prod.txt

EXPOSE 5050

# Run Application
CMD [ "sh", "-c", "python /app/main.py --env ${envType} > /app/console.log" ]