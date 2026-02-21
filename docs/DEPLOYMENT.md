# Deployment Strategy

## 1. Docker Compose (Development)

### docker-compose.yml
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: interview_db
      POSTGRES_USER: interview_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./migrations:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U interview_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # RabbitMQ Message Queue
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: interview
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Interview Service (Go)
  interview-service:
    build:
      context: ./services/interview-service
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: interview_db
      DB_USER: interview_user
      DB_PASSWORD: ${DB_PASSWORD}
      REDIS_HOST: redis:6379
      RABBITMQ_URL: amqp://interview:${RABBITMQ_PASSWORD}@rabbitmq:5672/
      EMOTION_SERVICE_URL: emotion-service:8081
      JWT_SECRET: ${JWT_SECRET}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    restart: unless-stopped

  # Emotion Service (Python)
  emotion-service:
    build:
      context: ./services/emotion-service
      dockerfile: Dockerfile
    ports:
      - "8081:8081"
    environment:
      REDIS_HOST: redis:6379
      RABBITMQ_URL: amqp://interview:${RABBITMQ_PASSWORD}@rabbitmq:5672/
      MODEL_PATH: /app/models
    volumes:
      - ./services/emotion-service/models:/app/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on:
      - redis
      - rabbitmq
    restart: unless-stopped

  # Scoring Service (Go)
  scoring-service:
    build:
      context: ./services/scoring-service
      dockerfile: Dockerfile
    ports:
      - "8082:8082"
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: interview_db
      DB_USER: interview_user
      DB_PASSWORD: ${DB_PASSWORD}
      REDIS_HOST: redis:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # Worker Service (Go)
  worker-service:
    build:
      context: ./services/worker-service
      dockerfile: Dockerfile
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: interview_db
      DB_USER: interview_user
      DB_PASSWORD: ${DB_PASSWORD}
      REDIS_HOST: redis:6379
      RABBITMQ_URL: amqp://interview:${RABBITMQ_PASSWORD}@rabbitmq:5672/
      EMOTION_SERVICE_URL: emotion-service:8081
      SCORING_SERVICE_URL: scoring-service:8082
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - emotion-service
      - scoring-service
    deploy:
      replicas: 3
    restart: unless-stopped

  # Nginx Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./infrastructure/docker/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - interview-service
      - emotion-service
      - scoring-service
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
```

## 2. Kubernetes (Production)

### Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ai-interview
```

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: ai-interview
data:
  DB_HOST: "postgres-service"
  DB_PORT: "5432"
  DB_NAME: "interview_db"
  REDIS_HOST: "redis-service:6379"
  RABBITMQ_URL: "amqp://rabbitmq-service:5672/"
```

### Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: ai-interview
type: Opaque
stringData:
  DB_PASSWORD: "your-db-password"
  JWT_SECRET: "your-jwt-secret"
  OPENAI_API_KEY: "your-openai-key"
  ANTHROPIC_API_KEY: "your-anthropic-key"
```

### Interview Service Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: interview-service
  namespace: ai-interview
spec:
  replicas: 3
  selector:
    matchLabels:
      app: interview-service
  template:
    metadata:
      labels:
        app: interview-service
    spec:
      containers:
      - name: interview-service
        image: your-registry/interview-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DB_HOST
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_PASSWORD
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: interview-service
  namespace: ai-interview
spec:
  selector:
    app: interview-service
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
  type: ClusterIP
```

### Emotion Service Deployment (GPU)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: emotion-service
  namespace: ai-interview
spec:
  replicas: 2
  selector:
    matchLabels:
      app: emotion-service
  template:
    metadata:
      labels:
        app: emotion-service
    spec:
      nodeSelector:
        accelerator: nvidia-tesla-t4
      containers:
      - name: emotion-service
        image: your-registry/emotion-service:latest
        ports:
        - containerPort: 8081
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: 1
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: emotion-service
  namespace: ai-interview
spec:
  selector:
    app: emotion-service
  ports:
  - protocol: TCP
    port: 8081
    targetPort: 8081
  type: ClusterIP
```

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: interview-service-hpa
  namespace: ai-interview
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: interview-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: ai-interview
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/websocket-services: "interview-service"
spec:
  tls:
  - hosts:
    - api.interview.com
    secretName: api-tls
  rules:
  - host: api.interview.com
    http:
      paths:
      - path: /api/v1/interviews
        pathType: Prefix
        backend:
          service:
            name: interview-service
            port:
              number: 8080
      - path: /api/v1/emotions
        pathType: Prefix
        backend:
          service:
            name: emotion-service
            port:
              number: 8081
      - path: /api/v1/scores
        pathType: Prefix
        backend:
          service:
            name: scoring-service
            port:
              number: 8082
```

## 3. CI/CD Pipeline (GitHub Actions)

### .github/workflows/ci.yml
```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-go:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'
    
    - name: Run tests
      run: |
        cd services/interview-service
        go test -v -race -coverprofile=coverage.out ./...
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.out

  test-python:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd services/emotion-service
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        cd services/emotion-service
        pytest --cov=app tests/

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: golangci-lint
      uses: golangci/golangci-lint-action@v3
      with:
        version: latest
        working-directory: services/interview-service
    
    - name: flake8
      run: |
        pip install flake8
        cd services/emotion-service
        flake8 app/

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

### .github/workflows/cd.yml
```yaml
name: CD Pipeline

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [interview-service, emotion-service, scoring-service, worker-service]
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ secrets.REGISTRY_URL }}
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ secrets.REGISTRY_URL }}/${{ matrix.service }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=sha
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: ./services/${{ matrix.service }}
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG }}
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f infrastructure/kubernetes/
        kubectl rollout status deployment/interview-service -n ai-interview
        kubectl rollout status deployment/emotion-service -n ai-interview
```

## 4. Terraform Infrastructure

### main.tf
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "interview-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr = "10.0.0.0/16"
  azs      = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# EKS Cluster
module "eks" {
  source = "./modules/eks"
  
  cluster_name    = "interview-cluster"
  cluster_version = "1.28"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  
  node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10
      instance_types = ["t3.large"]
    }
    gpu = {
      desired_size = 2
      min_size     = 1
      max_size     = 5
      instance_types = ["g4dn.xlarge"]
    }
  }
}

# RDS PostgreSQL
module "rds" {
  source = "./modules/rds"
  
  identifier     = "interview-db"
  engine_version = "15.3"
  instance_class = "db.t3.large"
  allocated_storage = 100
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.database_subnet_ids
  
  multi_az = true
  backup_retention_period = 7
}

# ElastiCache Redis
module "elasticache" {
  source = "./modules/elasticache"
  
  cluster_id      = "interview-redis"
  engine_version  = "7.0"
  node_type       = "cache.t3.medium"
  num_cache_nodes = 2
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.cache_subnet_ids
}

# S3 Bucket for video storage
resource "aws_s3_bucket" "videos" {
  bucket = "interview-videos-${var.environment}"
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    enabled = true
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}
```

## 5. Monitoring Setup

### Prometheus Configuration
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'interview-service'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - ai-interview
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: interview-service
      - source_labels: [__meta_kubernetes_pod_ip]
        target_label: __address__
        replacement: ${1}:8080

  - job_name: 'emotion-service'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - ai-interview
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: emotion-service
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "AI Interview Platform",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Active WebSocket Connections",
        "targets": [
          {
            "expr": "websocket_active_connections"
          }
        ]
      },
      {
        "title": "Queue Depth",
        "targets": [
          {
            "expr": "queue_depth"
          }
        ]
      }
    ]
  }
}
```

## 6. Backup & Disaster Recovery

### Backup Script
```bash
#!/bin/bash

# PostgreSQL Backup
pg_dump -h $DB_HOST -U $DB_USER -d interview_db | \
  gzip > /backups/db_$(date +%Y%m%d_%H%M%S).sql.gz

# Upload to S3
aws s3 cp /backups/db_*.sql.gz s3://interview-backups/database/

# Redis Backup
redis-cli --rdb /backups/redis_$(date +%Y%m%d_%H%M%S).rdb
aws s3 cp /backups/redis_*.rdb s3://interview-backups/redis/

# Cleanup old backups (keep last 30 days)
find /backups -name "*.gz" -mtime +30 -delete
find /backups -name "*.rdb" -mtime +30 -delete
```

## 7. Zero-Downtime Deployment

### Rolling Update Strategy
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  minReadySeconds: 30
  progressDeadlineSeconds: 600
```

### Blue-Green Deployment
```bash
# Deploy green version
kubectl apply -f deployment-green.yaml

# Wait for green to be ready
kubectl wait --for=condition=available --timeout=300s deployment/interview-service-green

# Switch traffic
kubectl patch service interview-service -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor for issues
sleep 300

# If successful, delete blue
kubectl delete deployment interview-service-blue
```
