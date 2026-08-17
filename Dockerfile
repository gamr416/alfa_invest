FROM node:22-alpine AS ui
WORKDIR /web
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY server/requirements.txt ./server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt
COPY server/ ./server/
COPY --from=ui /web/dist ./web/dist
WORKDIR /app/server
ENV OLLAMA_URL=http://127.0.0.1:1
EXPOSE 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
