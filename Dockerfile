from python:3-alpine

RUN apk add --no-cache curl
WORKDIR /app
ADD ./app/requirements.txt .
RUN pip install -r requirements.txt

ADD app /app

CMD ["python", "tempurasp.py"]

HEALTHCHECK --interval=15s --timeout=2s --retries=12 \
  CMD curl --fail localhost:8080 || exit 1
