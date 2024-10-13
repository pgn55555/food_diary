FROM python:3.11.0-alpine

WORKDIR /app

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD ["flask", "--app", "main", "run"]