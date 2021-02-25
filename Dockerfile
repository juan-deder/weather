FROM python:3.9-alpine
WORKDIR /app
RUN pip install --no-cache-dir flask flask-caching requests
COPY . .
ENV FLASK_ENV=development CACHE_TYPE=filesystem CACHE_DEFAULT_TIMEOUT=120 CACHE_DIR=/cache
CMD flask run -h 0.0.0.0