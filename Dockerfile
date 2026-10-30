# One image: the static web export served by the FastAPI app.
FROM node:22-slim AS web
WORKDIR /web
COPY web/package.json web/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY web/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY proofpay/ proofpay/
RUN pip install --no-cache-dir .
COPY demo/ demo/
COPY docs/ docs/
COPY --from=web /web/out web/out
ENV PROOFPAY_DB=/tmp/proofpay.db
EXPOSE 8000
CMD ["sh", "-c", "uvicorn proofpay.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
