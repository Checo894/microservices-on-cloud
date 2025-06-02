FROM python:3.10-slim
WORKDIR /microservicios
COPY multiplica.py .
RUN pip install fastapi uvicorn pydantic requests mysql-connector-python
CMD ["uvicorn", "multiplica:app", "--host", "0.0.0.0", "--port", "8000"]