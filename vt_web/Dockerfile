# Use a Python base image
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create a working directory
WORKDIR /opt/app

# Copy requirements.txt
COPY requirements.txt /opt/app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /opt/app/

# Set the entrypoint for the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "vt_web.wsgi:application"]
