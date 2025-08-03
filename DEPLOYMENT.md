# FastPrint Deployment Guide

This guide will help you deploy the FastPrint application on AWS EC2 with SSL and proper frontend-backend connectivity.

## 🚀 Quick Start

1. **Clone both repositories** on your EC2 instance:
   ```bash
   git clone https://github.com/AyanAhmed30/FastPrint.git
   git clone https://github.com/AyanAhmed30/FastPrint-Frontend.git
   ```

2. **Run the deployment script**:
   ```bash
   cd FastPrint
   ./deploy.sh
   ```

3. **Set up SSL certificates**:
   ```bash
   sudo certbot --nginx -d app.fastprintguys.com
   ```

## 📋 Prerequisites

### System Requirements
- Ubuntu 20.04+ or similar Linux distribution
- At least 2GB RAM and 20GB storage
- Domain name pointing to your EC2 instance
- Ports 80 and 443 open in security groups

### Required Software
- Docker and Docker Compose
- Nginx
- Node.js 18+ and npm
- Certbot for SSL certificates

### Installation Commands
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Nginx
sudo apt install -y nginx

# Install Certbot
sudo apt install -y certbot python3-certbot-nginx
```

## ⚙️ Configuration

### 1. Backend Configuration

Create and configure the environment file:
```bash
cd FastPrint
cp fastprint_backend/.env.production fastprint_backend/.env
```

Edit `fastprint_backend/.env` with your production values:
```env
DEBUG=False
DJANGO_SECRET_KEY=your-super-secret-production-key-here
DB_NAME=fastprint_db
DB_USER=fastprint_user
DB_PASSWORD=your-secure-database-password
DB_HOST=db
DB_PORT=3306
EC2_PUBLIC_IP=your-ec2-public-ip
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### 2. Frontend Configuration

The frontend is already configured to use `https://app.fastprintguys.com/api/` as the backend URL.

### 3. Database Setup

The Docker Compose configuration will automatically set up MySQL. Make sure to use strong passwords in your `.env` file.

## 🔧 Manual Deployment Steps

If you prefer to deploy manually instead of using the script:

### Backend Deployment

1. **Build and start backend services**:
   ```bash
   cd FastPrint
   docker-compose up -d --build
   ```

2. **Run database migrations**:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

3. **Create superuser** (optional):
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

4. **Collect static files**:
   ```bash
   docker-compose exec backend python manage.py collectstatic --noinput
   ```

### Frontend Deployment

1. **Build the frontend**:
   ```bash
   cd FastPrint-Frontend/fastprint-frontend
   npm ci
   npm run build
   ```

2. **Deploy with Docker** (recommended):
   ```bash
   docker build -t fastprint-frontend .
   docker run -d --name fastprint-frontend -p 3000:80 fastprint-frontend
   ```

### Nginx Configuration

1. **Copy nginx configuration**:
   ```bash
   sudo cp FastPrint/nginx/app.fastprintguys.com.conf /etc/nginx/sites-available/
   sudo ln -s /etc/nginx/sites-available/app.fastprintguys.com.conf /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default
   ```

2. **Test and restart nginx**:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### SSL Setup

1. **Install SSL certificate**:
   ```bash
   sudo certbot --nginx -d app.fastprintguys.com
   ```

2. **Set up auto-renewal**:
   ```bash
   sudo crontab -e
   # Add this line:
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

## 🔍 Troubleshooting

### Common Issues

#### 1. CORS Errors
- **Symptom**: Frontend can't connect to backend, CORS errors in browser console
- **Solution**: Check that `app.fastprintguys.com` is in Django's `CORS_ALLOWED_ORIGINS`
- **Verify**: Check `fastprint_backend/fastprint_backend/settings.py`

#### 2. 502 Bad Gateway
- **Symptom**: Nginx returns 502 error
- **Solution**: Check if backend is running on port 8000
- **Debug**: `docker-compose logs backend` and `sudo nginx -t`

#### 3. SSL Certificate Issues
- **Symptom**: SSL warnings or certificate errors
- **Solution**: Ensure domain points to correct IP and run certbot again
- **Debug**: `sudo certbot certificates`

#### 4. Database Connection Errors
- **Symptom**: Backend can't connect to database
- **Solution**: Check database credentials in `.env` file
- **Debug**: `docker-compose logs db`

### Useful Commands

```bash
# View logs
docker-compose logs backend
docker-compose logs db
docker logs fastprint-frontend
sudo tail -f /var/log/nginx/error.log

# Restart services
docker-compose restart
sudo systemctl restart nginx

# Check service status
docker-compose ps
sudo systemctl status nginx
sudo systemctl status certbot.timer

# Database operations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec db mysql -u root -p fastprint_db
```

## 🔒 Security Considerations

1. **Change default passwords** in `.env` file
2. **Use strong Django secret key**
3. **Keep system updated**: `sudo apt update && sudo apt upgrade`
4. **Monitor logs** regularly for suspicious activity
5. **Backup database** regularly:
   ```bash
   docker-compose exec db mysqldump -u root -p fastprint_db > backup.sql
   ```

## 📊 Monitoring

### Health Checks
- Backend: `https://app.fastprintguys.com/admin/`
- Frontend: `https://app.fastprintguys.com/`
- Health endpoint: `https://app.fastprintguys.com/health`

### Performance Monitoring
- Use `htop` to monitor system resources
- Check Docker stats: `docker stats`
- Monitor nginx access logs: `sudo tail -f /var/log/nginx/access.log`

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs using the commands provided
3. Ensure all prerequisites are installed correctly
4. Verify your domain DNS settings
5. Check AWS security group settings (ports 80, 443, 22)

## 📝 Notes

- The deployment uses Docker for containerization
- Nginx serves as a reverse proxy and handles SSL termination
- Static files are served directly by Nginx for better performance
- Database runs in a separate container with persistent storage
- Frontend is built as a static site and served through Nginx

## 🔄 Updates

To update the application:

1. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

2. **Rebuild and restart**:
   ```bash
   docker-compose up -d --build
   ```

3. **Update frontend**:
   ```bash
   cd FastPrint-Frontend/fastprint-frontend
   git pull origin main
   npm run build
   docker build -t fastprint-frontend .
   docker stop fastprint-frontend
   docker rm fastprint-frontend
   docker run -d --name fastprint-frontend -p 3000:80 fastprint-frontend
   ```
