from python:3-alpine

RUN apk add --no-cache curl

ADD app /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "tempurasp.py"]

HEALTHCHECK --interval=15s --timeout=2s --retries=12 \
  CMD curl --fail localhost:8080 || exit 1
