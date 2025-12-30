# Use an official Python runtime as a parent image
FROM public.ecr.aws/docker/library/python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libglib2.0-0 \
    libgirepository-1.0-1 \
    gir1.2-glib-2.0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*


    
# Create and set permissions for media and static directories
RUN mkdir -p /app/media /app/static \
    && chmod -R 755 /app

# Install Python dependencies
COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn
RUN pip install pandas openpyxl

# Copy project
COPY . /app/

# Set permissions for the app directory
RUN chown -R www-data:www-data /app \
    && chmod -R 755 /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && chown www-data:www-data /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]