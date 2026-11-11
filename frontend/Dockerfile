FROM python:3.12-slim

WORKDIR /app

# Permite que o Python encontre o pacote frontend dentro de /app.
ENV PYTHONPATH=/app

COPY requirements-frontend.txt .
RUN pip install --no-cache-dir -r requirements-frontend.txt

COPY frontend ./frontend

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501"]