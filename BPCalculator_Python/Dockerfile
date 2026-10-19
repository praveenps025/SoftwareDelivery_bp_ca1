FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# commit SHA, passed by the pipeline; sent back in the X-App-Version header
ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION

EXPOSE 5000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "--call", "app:create_app"]
