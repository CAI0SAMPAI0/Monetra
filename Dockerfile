# Stage 1: Build Tailwind CSS
FROM node:20-slim AS tailwind-builder
WORKDIR /app

# Copy the tailwind source code and templates to scan for utility classes
COPY theme/static_src/ /app/theme/static_src/
COPY frontend/templates/ /app/frontend/templates/
COPY theme/templates/ /app/theme/templates/

# Install dependencies and build Tailwind assets
WORKDIR /app/theme/static_src
RUN npm ci && npm run build

# Stage 2: Final runtime environment
FROM python:3.12-slim AS runner

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=core.settings.production \
    PORT=8000

WORKDIR /app

# Install system dependencies (curl for health checks, libpq-dev for DB connectivity if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# Copy theme templates and statically built tailwind css from stage 1
COPY theme/ /app/theme/
COPY --from=tailwind-builder /app/theme/static/css/dist/styles.css /app/theme/static/css/dist/styles.css

# Copy the rest of the application code
COPY . /app/

# Collect static files (disable active DB connection and secret key requirements during build)
RUN SECRET_KEY=dummy_secret_key_for_collectstatic \
    DATABASE_URL=sqlite:///:memory: \
    python manage.py collectstatic --noinput

# Run the app under a non-privileged user for security
RUN useradd -m -U appuser && chown -R appuser:appuser /app
USER appuser

# Expose Django port
EXPOSE 8000

# Start application with gunicorn after running migrations
CMD ["sh", "-c", "python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]
