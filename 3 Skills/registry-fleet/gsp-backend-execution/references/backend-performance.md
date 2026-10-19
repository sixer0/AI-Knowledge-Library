# Backend Performance Optimization

## Caching Strategies

### Cache-Aside (Recommended)
```typescript
export class ProductService {
  constructor(
    private db: PrismaClient,
    private cache: Redis,
  ) {}

  async getProduct(id: string) {
    // Try cache first
    const cached = await this.cache.get(`product:${id}`);
    if (cached) return JSON.parse(cached);

    // Cache miss - fetch from DB
    const product = await this.db.product.findUnique({ where: { id } });

    // Store in cache (5 min TTL)
    if (product) {
      await this.cache.setex(`product:${id}`, 300, JSON.stringify(product));
    }

    return product;
  }
}
```

### Write-Through
```typescript
async createProduct(data: CreateProductDTO) {
  const product = await this.db.product.create({ data });

  // Immediately update cache
  await this.cache.setex(`product:${product.id}`, 300, JSON.stringify(product));

  return product;
}
```

### Redis Cache Patterns

```typescript
import { Redis } from 'ioredis';

export class CacheService {
  constructor(private redis: Redis) {}

  // Simple get/set
  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: any, ttlSeconds = 300): Promise<void> {
    await this.redis.setex(key, ttlSeconds, JSON.stringify(value));
  }

  // Pattern-based invalidation
  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  // Distributed locking
  async withLock<T>(key: string, fn: () => Promise<T>, ttlSeconds = 30): Promise<T> {
    const lockKey = `lock:${key}`;
    const lock = await this.redis.set(lockKey, '1', 'EX', ttlSeconds, 'NX');

    if (!lock) {
      throw new Error(`Could not acquire lock for ${key}`);
    }

    try {
      return await fn();
    } finally {
      await this.redis.del(lockKey);
    }
  }

  // Cache with probabilistic early expiration
  async getOrSet<T>(key: string, fn: () => Promise<T>, ttlSeconds = 300): Promise<T> {
    const cached = await this.redis.get(key);
    if (cached) return JSON.parse(cached);

    const data = await fn();
    await this.redis.setex(key, ttlSeconds, JSON.stringify(data));
    return data;
  }
}
```

## Database Optimization

### Indexing Strategy
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index (smaller, faster)
CREATE INDEX idx_orders_pending ON orders(created_at) WHERE status = 'pending';

-- GIN index for JSON
CREATE INDEX idx_products_attrs ON products USING GIN(attributes);

-- Full-text search
CREATE INDEX idx_products_search ON products USING GIN(to_tsvector('english', name || ' ' || description));
```

### Query Optimization
```typescript
// ❌ N+1 query
const users = await prisma.user.findMany();
for (const user of users) {
  user.orders = await prisma.order.findMany({ where: { userId: user.id } });
}

// ✅ Eager loading
const users = await prisma.user.findMany({
  include: { orders: true },
});

// ✅ Select only needed fields
const emails = await prisma.user.findMany({
  select: { email: true },
});

// ✅ Pagination with keyset (faster than offset)
const orders = await prisma.order.findMany({
  take: 20,
  skip: 0,
  cursor: { id: lastSeenId },
  orderBy: { id: 'asc' },
});
```

### Connection Pooling
```typescript
// Prisma
const prisma = new PrismaClient({
  datasources: {
    db: { url: process.env.DATABASE_URL },
  },
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

// pg (node-postgres)
import { Pool } from 'pg';
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                  // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

## Load Balancing

```typescript
// Round Robin (default)
const servers = ['server1:3000', 'server2:3000', 'server3:3000'];
let current = 0;

function getNextServer(): string {
  const server = servers[current];
  current = (current + 1) % servers.length;
  return server;
}

// Least Connections
const serverLoads = new Map<string, number>();
// Route to server with lowest active connections
```

## CDN Integration

```typescript
// Cache static assets at CDN level
// Origin: your server
// CDN: CloudFlare, CloudFront, etc.

// Set cache headers for CDN
app.use('/static', express.static('public', {
  setHeaders: (res, path) => {
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
  },
}));

// API responses - don't cache at CDN
app.use('/api', (req, res, next) => {
  res.setHeader('Cache-Control', 'private, no-cache');
  next();
});
```

## Performance Monitoring

```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';

// OpenTelemetry tracing
const tracer = trace.getTracer('my-app');

async function getProduct(id: string) {
  return tracer.startActiveSpan('product.get', async (span) => {
    try {
      span.setAttribute('product.id', id);

      const product = await productService.getProduct(id);

      span.setStatus({ code: SpanStatusCode.OK });
      return product;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

## Metrics

```typescript
// Prometheus metrics
import { register, Counter, Histogram, Gauge } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10],
});

const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
});

// Usage
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.route.path, status_code: res.statusCode });
  });
  next();
});
```

## Scaling Patterns

### Horizontal Scaling
```
                    ┌─────────────┐
                    │ Load Balancer│
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
     ┌──────────┐    ┌──────────┐    ┌──────────┐
     │ Server 1 │    │ Server 2 │    │ Server 3 │
     └──────────┘    └──────────┘    └──────────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │   (Primary)  │
                    └──────────────┘
```

### Database Read Replicas
```typescript
const prismaRead = new PrismaClient({
  datasources: { db: { url: process.env.DATABASE_URL_READ_REPLICA } },
});

const prismaWrite = new PrismaClient({
  datasources: { db: { url: process.env.DATABASE_URL_WRITE } },
});

// Use read replica for reads, primary for writes
async function getUser(id: string) {
  return prismaRead.user.findUnique({ where: { id } });
}

async function createUser(data: any) {
  return prismaWrite.user.create({ data });
}
```