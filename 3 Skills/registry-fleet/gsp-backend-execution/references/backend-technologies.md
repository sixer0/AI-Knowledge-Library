# Backend Technologies Reference

## Languages

| Language | Best For | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **Node.js/TypeScript** | Full-stack, APIs, real-time | Same language end-to-end, huge ecosystem, async I/O | CPU-intensive tasks suffer |
| **Python** | Data/ML, rapid development | Rich ML libraries, readable, fast prototyping | GIL limits concurrency, slower runtime |
| **Go** | Microservices, concurrency | Excellent concurrency (goroutines), fast, simple | Verbose error handling, no generics (pre-1.21) |
| **Rust** | Performance-critical | Memory safety without GC, fastest | Steep learning curve, slow compile times |

## Frameworks

### Node.js
| Framework | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **NestJS** | Enterprise APIs | TypeScript-first, decorators, DI, modular | Heavy, opinionated |
| **Express** | Lightweight APIs | Minimal, flexible, middleware ecosystem | No structure enforcement |
| **Fastify** | High-performance | Faster than Express, schema validation | Smaller ecosystem |
| **Hono** | Edge functions | Lightweight, works everywhere | Newer, smaller community |

### Python
| Framework | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **FastAPI** | Modern APIs | Async, auto-docs, Pydantic validation | Less mature than Django |
| **Django** | Full-stack | Batteries included, ORM, admin | Heavy, synchronous |
| **Flask** | Lightweight | Minimal, flexible | No structure enforcement |

### Go
| Framework | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **Gin** | APIs | Fast, lightweight, middleware | No DI container |
| **Echo** | APIs | Fast, simple, middleware | Less popular than Gin |
| **Fiber** | Performance | Express-like, fastest Go framework | Newer, less battle-tested |

## Databases

### Relational (SQL)
| Database | Best For | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **PostgreSQL** | Primary data store | ACID, JSON support, full-text search, GIS | Requires tuning |
| **MySQL** | Web apps | Fast reads, Replication | Less feature-rich than PG |
| **SQLite** | Embedded/local | Zero config, file-based | Concurrency limited |

### Document (NoSQL)
| Database | Best For | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **MongoDB** | Flexible schemas | Dynamic schema, aggregation | No transactions across collections |
| **Firebase** | Mobile/backends | Real-time, serverless | Vendor lock-in |

### Cache
| Solution | Best For | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **Redis** | Caching, sessions, pub/sub | In-memory speed, data structures | Memory-dependent |
| **Memcached** | Simple caching | Very fast, simple | No persistence, no data structures |

## Message Queues

| Queue | Best For | Strengths | Weaknesses |
|-------|----------|-----------|------------|
| **RabbitMQ** | Standard messaging | Reliable, many patterns | Manual cluster management |
| **Kafka** | Event streaming | High throughput, durability | Complex setup |
| **BullMQ** | Job queues | Redis-based, retry logic | Redis dependency |
| **SQS** | Serverless | Fully managed, scales | No pub/sub patterns |

## ORMs

| ORM | Language | Strengths | Weaknesses |
|-----|----------|-----------|------------|
| **Prisma** | TypeScript | Type-safe, migrations, DX | Less flexible than raw SQL |
| **Drizzle** | TypeScript | Lightweight, SQL-like, fast | Smaller ecosystem |
| **Sequelize** | TypeScript | Many databases, mature | Callback-heavy, slower |
| **SQLAlchemy** | Python | Powerful, flexible | Complex for beginners |
| **GORM** | Go | Simple, automigrate | Less idiomatic Go |

## Caching Strategies

### Cache-Aside (Lazy Loading)
```
1. Check cache first
2. If miss, fetch from DB
3. Store in cache with TTL
4. Return data
```

### Write-Through
```
1. Write to cache AND DB simultaneously
2. Cache always fresh
3. Higher write latency
```

### Write-Behind
```
1. Write to cache only
2. Async write to DB
3. Risk of data loss
```

## Connection Pooling

```typescript
// Prisma
const prisma = new PrismaClient({
  datasources: { db: { url: process.env.DATABASE_URL } },
  log: ['query', 'error', 'warn'],
});

// pg (node-postgres)
import { Pool } from 'pg';
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

## When to Use What

| Scenario | Recommendation |
|----------|----------------|
| Rapid API development | Node.js + Fastify or NestJS |
| ML/Data processing | Python + FastAPI |
| High-concurrency microservices | Go + Gin |
| Maximum performance | Rust + Axum |
| ACID transactions required | PostgreSQL |
| Flexible schema/document storage | MongoDB |
| Session/token caching | Redis |
| Background job processing | BullMQ or Kafka |
| Serverless functions | SQS + Lambda or Firebase |