# Backend DevOps

## Docker

### Dockerfile (Node.js)
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodeuser -u 1001
COPY --from=builder --chown=nodeuser:nodejs /app/dist ./dist
COPY --from=builder --chown=nodeuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodeuser:nodejs /app/package.json ./

USER nodeuser
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Kubernetes

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: myapp/api:latest
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## CI/CD

### GitHub Actions
```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: myapp/api:${{ github.sha }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: api-service
          image: gcr.io/myapp/api:${{ github.sha }}
```

## Deployment Strategies

### Blue-Green Deployment
```yaml
# Deploy new version alongside old
# Traffic switches after healthy validation

apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
    slot: production  # Switch this to 'blue' or 'green'
---
# Two deployments with slot label
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
        slot: blue
```

### Canary Deployment
```yaml
# Gradually shift traffic to new version

apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 3000
---
# Original version (80% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-v1
spec:
  replicas: 10  # 80%
  template:
    metadata:
      labels:
        app: api
        version: v1
---
# Canary version (20% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-v2
spec:
  replicas: 2  # 20%
  template:
    metadata:
      labels:
        app: api
        version: v2
```

## Monitoring

### Prometheus Metrics
```typescript
import { register, Counter, Histogram, Gauge } from 'prom-client';

// Request duration
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.3, 0.5, 1, 3, 5],
});

// Active connections
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
});

// Error count
const errorCount = new Counter({
  name: 'errors_total',
  help: 'Total number of errors',
  labelNames: ['type', 'endpoint'],
});

// Express middleware
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  activeConnections.inc();
  res.on('finish', () => {
    end({ method: req.method, route: req.route?.path, status_code: res.statusCode });
    activeConnections.dec();
  });
  next();
});
```

### Health Checks
```typescript
// Liveness probe (is the process alive?)
app.get('/health/live', (req, res) => {
  res.json({ status: 'ok' });
});

// Readiness probe (can it serve traffic?)
app.get('/health/ready', async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    await redis.ping();
    res.json({ status: 'ok', checks: { db: 'ok', cache: 'ok' } });
  } catch (error) {
    res.status(503).json({ status: 'error', error: error.message });
  }
});
```

## Logging

### Structured Logging
```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Usage
logger.info({
  correlationId: req.correlationId,
  event: 'request.completed',
  method: req.method,
  path: req.path,
  statusCode: res.statusCode,
  duration: performance.now() - start,
  userId: req.user?.id,
});
```

### Log Levels
| Level | Usage |
|-------|-------|
| **fatal** | Unrecoverable, system crash |
| **error** | Recoverable errors, needs attention |
| **warn** | Potential issues, degraded operation |
| **info** | Normal operation events |
| **debug** | Detailed debugging info (prod: off) |
| **trace** | Very detailed (sql queries, etc.) |