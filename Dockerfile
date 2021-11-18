FROM python:3.9-alpine AS BUILDER
RUN apk update && apk add build-base

COPY . /code/
WORKDIR /code
RUN pip install --user -r requirements.txt

FROM python:3.9-alpine

COPY --from=BUILDER /code/ /code
COPY --from=BUILDER /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=BUILDER /usr/local/bin/gunicorn /usr/local/bin/gunicorn
WORKDIR /code

#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
ENTRYPOINT [ "gunicorn", "--bind :$PORT", "--workers 1", "--threads 8", "app:app" ]