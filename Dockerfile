FROM python:3.7.6-alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install -r requirements.txt

CMD ["python", "misfitbot.py"]
