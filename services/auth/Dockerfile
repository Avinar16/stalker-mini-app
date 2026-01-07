FROM python:3.12-slim

WORKDIR /app

COPY auth .
COPY utils ../utils/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ../utils/settings
RUN pip install ../utils/auth_utils



CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --reload --host 0.0.0.0 --port 8000"]