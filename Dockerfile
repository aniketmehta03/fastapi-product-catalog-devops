# -------- Builder Stage --------
FROM python:3.12-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# -------- Final Stage --------
FROM python:3.12-slim

# create non-root user
RUN useradd -m appuser

WORKDIR /app

# copy installed deps
COPY --from=builder /install /usr/local

# copy app code
COPY . .

# change ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
