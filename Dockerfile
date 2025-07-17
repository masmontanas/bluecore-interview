FROM python:3.11-slim


RUN groupadd -g 10001 appuser && \
    useradd -m -u 10001 -g 10001 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY config.yaml .

USER appuser

CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8080", \
     "--log-level", "critical", \
     "--access-logfile", "/dev/null", \
     "--error-logfile", "/dev/null"]
