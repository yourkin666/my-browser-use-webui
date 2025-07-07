FROM python:3.11-slim

# Set platform for multi-arch builds
ARG TARGETPLATFORM
ARG NODE_MAJOR=20

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    netcat-traditional \
    gnupg \
    curl \
    unzip \
    xvfb \
    libnss3 \
    libnspr4 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libgconf-2-4 \
    fonts-liberation \
    supervisor \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for some playwright dependencies)
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install nodejs -y \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-browsers
RUN mkdir -p $PLAYWRIGHT_BROWSERS_PATH
RUN playwright install chromium --with-deps

# Copy the application code
COPY . .

# Set up supervisor configuration
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create tmp directory for downloads
RUN mkdir -p /app/tmp/downloads

# Expose ports
EXPOSE 7788

# Set environment variables
ENV DISPLAY=:99
ENV PYTHONPATH=/app

# Run the application
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]