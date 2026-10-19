# Backend Debugging

## Logging Best Practices

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

// ❌ Don't do this
console.log('User created', user);
console.error('Error occurred');

// ✅ Do this - structured with context
logger.info({
  correlationId: req.correlationId,
  event: 'user.created',
  userId: user.id,
  email: user.email,
  ip: req.ip,
});

logger.error({
  correlationId: req.correlationId,
  event: 'user.creation_failed',
  error: err.message,
  stack: err.stack,
  userId: req.body.email,
});
```

### Request Logging Middleware
```typescript
export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();

  res.on('finish', () => {
    logger.info({
      correlationId: req.correlationId,
      event: 'http.request',
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: Date.now() - start,
      userAgent: req.headers['user-agent'],
      ip: req.ip,
      userId: req.user?.id,
    });
  });

  next();
}
```

## Debugging Strategies

### 1. Reproduce the Issue
```typescript
// Always start with a minimal reproduction
// ❌ Don't guess the cause

// ✅ Test the exact scenario
test('should fail when user has no permissions', async () => {
  const user = await createUserWithNoPermissions();
  const response = await request(app)
    .delete(`/users/${user.id}`)
    .set('Authorization', `Bearer ${user.token}`);

  expect(response.status).toBe(403);
});
```

### 2. Add Debug Logging
```typescript
// Temporarily add verbose logging
async function getUser(id: string) {
  logger.debug({ userId: id, event: 'user.get.start' });

  const user = await userRepo.findById(id);

  logger.debug({ userId: id, user, event: 'user.get.found' });

  if (!user) {
    logger.warn({ userId: id, event: 'user.get.not_found' });
  }

  return user;
}
```

### 3. Use Correlation IDs
```typescript
// Every request gets a correlation ID for tracing
app.use((req, res, next) => {
  req.correlationId = (req.headers['x-correlation-id'] as string) || randomUUID();
  res.setHeader('x-correlation-id', req.correlationId);
  next();
});

// Log with correlation ID
logger.info({
  correlationId: req.correlationId,
  event: 'processing_request',
  requestId: req.correlationId,
});
```

## Common Issues & Solutions

### Memory Leaks
```typescript
// Symptoms: Memory grows over time, OOM restarts

// Debug with Node.js built-in heap snapshot
if (process.env.TAKE_HEAP_SNAPSHOT) {
  const v8 = require('v8');
  const fs = require('fs');
  const filename = `heap-${Date.now()}.heapsnapshot`;
  const snapshotStream = v8.writeHeapSnapshot(filename);
  logger.info({ event: 'heap_snapshot', filename });
}

// Check for event listener leaks
process.on('warning', (warning) => {
  if (warning.name === 'MaxListenersExceededWarning') {
    logger.warn({ event: 'max_listeners_exceeded', warning: warning.message });
  }
});
```

### Connection Pool Exhaustion
```typescript
// Symptoms: Requests hang, "too many connections" errors

// Monitor pool stats
const pool = new Pool({ max: 20 });

setInterval(() => {
  logger.info({
    event: 'pool_stats',
    total: pool.totalCount,
    idle: pool.idleCount,
    waiting: pool.waitingCount,
  });
}, 30000);

// Check for unclosed connections
pool.on('error', (err) => {
  logger.error({ event: 'pool_error', error: err.message });
});
```

### N+1 Query Problems
```typescript
// Debug: Log all queries in development
const prisma = new PrismaClient({
  log: [
    { emit: 'event', level: 'query' },
  ],
});

prisma.$on('query', (e) => {
  logger.debug({
    event: 'db_query',
    query: e.query,
    params: e.params,
    duration: e.duration,
  });
});

// Or use Prisma query logging
prisma.$on('query', (e) => {
  if (e.duration > 100) { // Slow query threshold
    logger.warn({
      event: 'slow_query',
      query: e.query,
      duration: e.duration,
    });
  }
});
```

## Performance Profiling

### CPU Profiling
```typescript
// Start CPU profile
import { profiler } from 'v8';

profiler.startProfiling('cpu-profile');

setTimeout(() => {
  const profile = profiler.stopProfiling();
  require('fs').writeFileSync(
    'profile.cpuprofile',
    JSON.stringify(profile)
  );
  logger.info({ event: 'profile_saved', filename: 'profile.cpuprofile' });
}, 30000); // Profile for 30 seconds
```

### Memory Profiling
```typescript
// Take heap snapshot
import v8 from 'v8';

function takeHeapSnapshot() {
  const filename = `heap-${Date.now()}.heapsnapshot`;
  const filepath = v8.writeHeapSnapshot(filename);
  logger.info({ event: 'heap_snapshot', filepath });
  return filepath;
}

// Expose via secret endpoint
app.post('/admin/heap-snapshot', authenticate, authorize('admin'), (req, res) => {
  try {
    const filepath = takeHeapSnapshot();
    res.json({ success: true, filepath });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

## Debugging Endpoints

```typescript
// Debug info endpoint (protect in production!)
app.get('/debug/info', authenticate, authorize('admin'), (req, res) => {
  res.json({
    pid: process.pid,
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    cpu: process.cpuUsage(),
    env: {
      nodeVersion: process.version,
      env: process.env.NODE_ENV,
    },
  });
});

// Active connections
app.get('/debug/connections', authenticate, authorize('admin'), (req, res) => {
  res.json({
    pool: {
      total: pool.totalCount,
      idle: pool.idleCount,
      waiting: pool.waitingCount,
    },
    redis: {
      connected: redis.status === 'ready',
    },
  });
});
```

## Remote Debugging

### Node.js Inspector
```bash
# Start with inspector
node --inspect=0.0.0.0:9229 dist/main.js

# Or for Docker
docker run -p 3000:3000 -p 9229:9229 myapp:latest node --inspect=0.0.0.0:9229 dist/main.js
```

### VS Code Debug Config
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Process",
      "port": 9229,
      "restart": true,
      "preLaunchTask": "npm:build"
    }
  ]
}
```

## Error Tracking

### Sentry Integration
```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  correlations: true,
});

// Capture errors
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    contexts: {
      user: { id: req.user?.id, email: req.user?.email },
      request: { url: req.url, method: req.method },
    },
  });
  throw error;
}
```

### Custom Error Reporter
```typescript
interface ErrorReport {
  error: Error;
  context: {
    userId?: string;
    correlationId: string;
    endpoint: string;
    method: string;
    requestBody?: unknown;
  };
}

async function reportError(report: ErrorReport) {
  // Send to error tracking service
  await Promise.all([
    Sentry.captureException(report.error, { contexts: report.context }),
    logger.error({
      ...report.context,
      event: 'error_reported',
      error: report.error.message,
      stack: report.error.stack,
    }),
  ]);
}
```

## Debugging Checklist

- [ ] Enable debug logging for the affected area
- [ ] Add correlation IDs to trace requests
- [ ] Reproduce the issue consistently
- [ ] Isolate the failing component
- [ ] Check logs for patterns (same error repeated?)
- [ ] Verify external dependencies (DB, cache, APIs)
- [ ] Check resource usage (memory, connections)
- [ ] Profile if performance issue
- [ ] Create minimal reproduction test
- [ ] Document the root cause and fix