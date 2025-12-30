#!/bin/sh

echo "Running Django migrations..."
python manage.py migrate --noinput

# echo "Checking AWS configuration..."
# echo "AWS_ACCESS_KEY_ID is set: $([ ! -z "$AWS_ACCESS_KEY_ID" ] && echo 'YES' || echo 'NO')"
# echo "AWS_STORAGE_BUCKET_NAME: $AWS_STORAGE_BUCKET_NAME"
# echo "AWS_S3_REGION_NAME: $AWS_S3_REGION_NAME"
# echo "AWS_S3_CUSTOM_DOMAIN: $AWS_S3_CUSTOM_DOMAIN"

echo "Collecting static files..."
# python manage.py collectstatic --noinput
python manage.py setup_admin --username admin --password I7XHLfPk24Bi --name "SuperAdmin"

# python manage.py setup_roles
# python manage.py load_initial_categories


echo "Starting Gunicorn..."
gunicorn Sandbird.wsgi:application --bind 0.0.0.0:80
