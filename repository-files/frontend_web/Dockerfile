# iLuminara-Core Frontend Dockerfile
# Multi-stage build for optimized Compassionate CHW Interface
# Compliance: NIST RMF supply chain requirements (pinned SHA hashes)

# Stage 1: Build
FROM node:20.11.0-alpine@sha256:bf77dc26e48ea95fca9d1aceb5acfa69d2e546b765ec2abfb502975f1a2d4def AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with audit
RUN npm ci --only=production && \
    npm audit fix && \
    npm cache clean --force

# Copy source code
COPY . .

# Build Flutter web app
RUN npm run build

# Stage 2: Production
FROM nginx:1.25.3-alpine@sha256:6a2f8b28e45c4adea04ec207a251fd4a2df03ddc930f782af51e315ebc76e9a9

# Install security updates
RUN apk update && \
    apk upgrade && \
    apk add --no-cache ca-certificates && \
    rm -rf /var/cache/apk/*

# Copy built assets from builder
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create non-root user
RUN addgroup -g 1001 -S iluminara && \
    adduser -S -D -H -u 1001 -h /usr/share/nginx/html -s /sbin/nologin -G iluminara -g iluminara iluminara && \
    chown -R iluminara:iluminara /usr/share/nginx/html && \
    chown -R iluminara:iluminara /var/cache/nginx && \
    chown -R iluminara:iluminara /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R iluminara:iluminara /var/run/nginx.pid

# Switch to non-root user
USER iluminara

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Labels for compliance
LABEL org.opencontainers.image.title="iLuminara Frontend" \
      org.opencontainers.image.description="Compassionate CHW Interface" \
      org.opencontainers.image.vendor="iLuminara Health" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.licenses="Proprietary" \
      compliance.gdpr="true" \
      compliance.hipaa="true" \
      compliance.kdpa="true"

CMD ["nginx", "-g", "daemon off;"]
