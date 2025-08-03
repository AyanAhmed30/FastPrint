#!/bin/bash

# FastPrint Deployment Script
# This script helps deploy the FastPrint application on AWS EC2

set -e  # Exit on any error

echo "🚀 FastPrint Deployment Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Check if .env file exists
if [ ! -f "fastprint_backend/.env" ]; then
    print_warning ".env file not found in fastprint_backend/"
    print_status "Creating .env file from template..."
    cp fastprint_backend/.env.production fastprint_backend/.env
    print_warning "Please edit fastprint_backend/.env with your production values before continuing"
    read -p "Press Enter after you've updated the .env file..."
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
print_status "Checking dependencies..."

if ! command_exists docker; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists docker-compose; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if ! command_exists nginx; then
    print_warning "Nginx is not installed. Installing nginx..."
    sudo apt update
    sudo apt install -y nginx
fi

# Stop existing services
print_status "Stopping existing services..."
sudo systemctl stop nginx || true
docker-compose down || true

# Build and start backend services
print_status "Building and starting backend services..."
docker-compose up -d --build

# Wait for backend to be ready
print_status "Waiting for backend to be ready..."
sleep 30

# Check if backend is running
if ! curl -f http://localhost:8000/admin/ >/dev/null 2>&1; then
    print_error "Backend is not responding. Check docker logs:"
    docker-compose logs backend
    exit 1
fi

# Setup nginx configuration
print_status "Setting up Nginx configuration..."
sudo cp nginx/app.fastprintguys.com.conf /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/app.fastprintguys.com.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
print_status "Testing Nginx configuration..."
if ! sudo nginx -t; then
    print_error "Nginx configuration test failed"
    exit 1
fi

# Create directories for static and media files
print_status "Creating directories for static and media files..."
sudo mkdir -p /var/www/fastprint/static
sudo mkdir -p /var/www/fastprint/media
sudo chown -R www-data:www-data /var/www/fastprint

# Collect static files
print_status "Collecting static files..."
docker-compose exec backend python manage.py collectstatic --noinput

# Copy static files to nginx directory
print_status "Copying static files to nginx directory..."
docker cp $(docker-compose ps -q backend):/app/static/. /var/www/fastprint/static/
sudo chown -R www-data:www-data /var/www/fastprint/static

# Start nginx
print_status "Starting Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

# Build and deploy frontend
print_status "Building and deploying frontend..."
cd fastprint-frontend

# Install dependencies and build
npm ci
npm run build

# Start frontend container (if using Docker)
if [ -f "Dockerfile" ]; then
    docker build -t fastprint-frontend .
    docker run -d --name fastprint-frontend -p 3000:80 fastprint-frontend
fi

cd ..

# Final checks
print_status "Performing final checks..."

# Check if services are running
if ! curl -f http://localhost:8000/admin/ >/dev/null 2>&1; then
    print_error "Backend health check failed"
    exit 1
fi

if ! curl -f http://localhost:3000/ >/dev/null 2>&1; then
    print_error "Frontend health check failed"
    exit 1
fi

if ! sudo nginx -t; then
    print_error "Nginx configuration is invalid"
    exit 1
fi

print_status "✅ Deployment completed successfully!"
print_status ""
print_status "Next steps:"
print_status "1. Make sure your domain points to this server's IP"
print_status "2. Set up SSL certificates with: sudo certbot --nginx -d app.fastprintguys.com"
print_status "3. Test your application at: https://app.fastprintguys.com"
print_status ""
print_status "Useful commands:"
print_status "- View backend logs: docker-compose logs backend"
print_status "- View frontend logs: docker logs fastprint-frontend"
print_status "- View nginx logs: sudo tail -f /var/log/nginx/error.log"
print_status "- Restart services: docker-compose restart"
