# Use official Python image
FROM python:3.10.7

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set up build arguments
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=autobin.settings.prod

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "autobin.wsgi:application"]
