FROM python:3.12-alpine

WORKDIR /app

# For health check
RUN apk update
RUN apk add curl

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "app.py"]
