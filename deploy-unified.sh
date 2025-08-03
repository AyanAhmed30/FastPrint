#!/bin/bash

# Unified FastPrint Deployment Script
# This script coordinates both frontend and backend deployments
# Can be used by both GitHub Actions and manual deployments

set -e  # Exit on any error

echo "🚀 FastPrint Unified Deployment Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Configuration
BACKEND_DIR="$HOME/FastPrint"
FRONTEND_DIR="$HOME/FastPrint-Frontend"
NGINX_CONFIG_DIR="/etc/nginx/sites-available"
DOMAIN="app.fastprintguys.com"

# Parse command line arguments
DEPLOY_BACKEND=true
DEPLOY_FRONTEND=true
SKIP_NGINX_RELOAD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            DEPLOY_FRONTEND=false
            shift
            ;;
        --frontend-only)
            DEPLOY_BACKEND=false
            shift
            ;;
        --skip-nginx-reload)
            SKIP_NGINX_RELOAD=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Function to check if a service is healthy
check_service_health() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    print_status "Checking $service_name health at $url..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            print_status "$service_name is healthy!"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts: $service_name not ready yet, waiting..."
        sleep 2
        ((attempt++))
    done
    
    print_error "$service_name health check failed after $max_attempts attempts"
    return 1
}

# Function to validate nginx configuration
validate_nginx_config() {
    print_step "Validating Nginx configuration..."
    if sudo nginx -t; then
        print_status "Nginx configuration is valid"
        return 0
    else
        print_error "Nginx configuration validation failed"
        return 1
    fi
}

# Function to reload nginx safely
reload_nginx() {
    if [ "$SKIP_NGINX_RELOAD" = true ]; then
        print_warning "Skipping Nginx reload as requested"
        return 0
    fi

    print_step "Reloading Nginx configuration..."
    if validate_nginx_config; then
        sudo systemctl reload nginx
        print_status "Nginx reloaded successfully"
        return 0
    else
        print_error "Nginx reload failed due to configuration errors"
        return 1
    fi
}

# Function to deploy backend
deploy_backend() {
    print_step "Deploying Backend..."
    
    cd "$BACKEND_DIR"
    
    # Pull latest changes
    print_status "Pulling latest backend changes..."
    git pull origin main
    
    # Stop existing containers gracefully
    print_status "Stopping existing backend containers..."
    docker-compose down --timeout 30
    
    # Build and start new containers
    print_status "Building and starting backend containers..."
    docker-compose up -d --build
    
    # Wait for backend to be ready
    print_status "Waiting for backend to be ready..."
    sleep 30
    
    # Run database migrations
    print_status "Running database migrations..."
    docker-compose exec -T backend python manage.py migrate
    
    # Collect static files
    print_status "Collecting static files..."
    docker-compose exec -T backend python manage.py collectstatic --noinput
    
    # Copy static files to nginx directory
    print_status "Copying static files to nginx directory..."
    sudo mkdir -p /var/www/fastprint/static
    sudo mkdir -p /var/www/fastprint/media
    
    # Get the backend container ID and copy static files
    BACKEND_CONTAINER=$(docker-compose ps -q backend)
    if [ ! -z "$BACKEND_CONTAINER" ]; then
        docker cp "$BACKEND_CONTAINER:/app/static/." /var/www/fastprint/static/ 2>/dev/null || true
        sudo chown -R www-data:www-data /var/www/fastprint
    fi
    
    # Health check
    if ! check_service_health "http://localhost:8000/admin/" "Backend"; then
        print_error "Backend deployment failed health check"
        return 1
    fi
    
    print_status "Backend deployment completed successfully!"
}

# Function to deploy frontend
deploy_frontend() {
    print_step "Deploying Frontend..."
    
    # Check if frontend directory exists
    if [ ! -d "$FRONTEND_DIR" ]; then
        print_error "Frontend directory not found at: $FRONTEND_DIR"
        print_error "Please check your folder structure and update the FRONTEND_DIR variable"
        return 1
    fi
    
    cd "$FRONTEND_DIR"
    
    # Pull latest changes
    print_status "Pulling latest frontend changes..."
    git pull origin main
    
    # Navigate to the actual frontend app directory
    cd fastprint-frontend
    print_status "Current directory: $(pwd)"
    
    # Stop existing frontend container
    print_status "Stopping existing frontend container..."
    docker stop fastprint-frontend 2>/dev/null || true
    docker rm fastprint-frontend 2>/dev/null || true
    
    # Build new frontend image
    print_status "Building frontend Docker image..."
    docker build -t fastprint-frontend .
    
    # Start new frontend container on port 3000 (as expected by Nginx)
    print_status "Starting frontend container..."
    docker run -d --name fastprint-frontend -p 3000:80 fastprint-frontend
    
    # Health check
    if ! check_service_health "http://localhost:3000/" "Frontend"; then
        print_error "Frontend deployment failed health check"
        return 1
    fi
    
    print_status "Frontend deployment completed successfully!"
}

# Function to validate full application
validate_application() {
    print_step "Validating full application through Nginx..."
    
    # Check if domain resolves to HTTPS
    if check_service_health "https://$DOMAIN/" "Frontend (via HTTPS)"; then
        print_status "Frontend is accessible via HTTPS"
    else
        print_warning "Frontend HTTPS check failed - this might be expected if SSL is not yet configured"
    fi
    
    # Check API endpoint
    if check_service_health "https://$DOMAIN/api/admin/" "Backend API (via HTTPS)"; then
        print_status "Backend API is accessible via HTTPS"
    else
        print_warning "Backend API HTTPS check failed - this might be expected if SSL is not yet configured"
    fi
    
    # Check HTTP redirects (should redirect to HTTPS)
    if curl -s -I "http://$DOMAIN/" | grep -q "301\|302"; then
        print_status "HTTP to HTTPS redirect is working"
    else
        print_warning "HTTP to HTTPS redirect check failed"
    fi
}

# Main deployment process
main() {
    print_status "Starting unified deployment process..."
    print_status "Backend deployment: $DEPLOY_BACKEND"
    print_status "Frontend deployment: $DEPLOY_FRONTEND"
    
    # Deploy backend if requested
    if [ "$DEPLOY_BACKEND" = true ]; then
        if ! deploy_backend; then
            print_error "Backend deployment failed"
            exit 1
        fi
    fi
    
    # Deploy frontend if requested
    if [ "$DEPLOY_FRONTEND" = true ]; then
        if ! deploy_frontend; then
            print_error "Frontend deployment failed"
            exit 1
        fi
    fi
    
    # Reload Nginx configuration
    if ! reload_nginx; then
        print_error "Nginx reload failed"
        exit 1
    fi
    
    # Final validation
    validate_application
    
    print_status "✅ Unified deployment completed successfully!"
    print_status ""
    print_status "🌐 Your application should be available at:"
    print_status "   Frontend: https://$DOMAIN"
    print_status "   Backend API: https://$DOMAIN/api/"
    print_status "   Admin Panel: https://$DOMAIN/admin/"
    print_status ""
    print_status "📋 Useful commands:"
    print_status "   Backend logs: docker-compose -f $BACKEND_DIR/docker-compose.yml logs backend"
    print_status "   Frontend logs: docker logs fastprint-frontend"
    print_status "   Nginx logs: sudo tail -f /var/log/nginx/error.log"
    print_status "   Restart services: $0"
}

# Run main function
main "$@"
