---
name: gsp-backend-execution
version: 1.0.1
description: >-
  Production-grade backend implementation skill for Node.js/TypeScript APIs.
  Covers clean architecture (layered/DDD), DRY principles, security hardening,
  and performance optimization. Use when implementing REST APIs, GraphQL resolvers,
  microservices, or backend services that require production readiness.
  Note: Error logging with persistence is defined in coder-execution agent.
license: MIT

metadata:
  hermes:
    tags: [gsp, development]
    category: development
---

# Backend Execution Skill

Production-ready backend implementation following clean architecture, security best practices, and performance standards.

---


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Berlaku atas **artefak tulis** skill ini (README, komentar/docstring, changelog, laporan review, spesifikasi API); kaidah pemrograman tidak diubah.
Kontrak keluaran seragam: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) **Module L** - L.2 header-metadata (`title,date,author_profile,status,task_ref,source_refs`),
L.3 heading bernomor + berkas `snake_case` (dokumen DATUM TERBIT/SERAH ikut DT-12), L.4 angka wajib `[R-n, sumber, hal]`, L.5 bahasa mengikuti user, L.6 checklist pra-serah (Module F.1) sebelum menyerahkan.
Konflik FORMAT → Module L menang; konflik GAYA presisi → Module H/K tetap menang.
## Technology Selection

**Languages:** Node.js/TypeScript (full-stack), Python (data/ML), Go (concurrency), Rust (performance)
**Frameworks:** NestJS, FastAPI, Django, Express, Gin
**Databases:** PostgreSQL (ACID), MongoDB (flexible schema), Redis (caching)
**APIs:** REST (simple), GraphQL (flexible), gRPC (performance)

### Quick Decision Matrix

| Need | Choose |
|------|--------|
| Fast development | Node.js + NestJS |
| Data/ML integration | Python + FastAPI |
| High concurrency | Go + Gin |
| Max performance | Rust + Axum |
| ACID transactions | PostgreSQL |
| Flexible schema | MongoDB |
| Caching | Redis |
| Internal services | gRPC |
| Public APIs | GraphQL/REST |
| Real-time events | Kafka |

## Key Best Practices (2025)

**Security:** Argon2id passwords, parameterized queries (98% SQL injection reduction), OAuth 2.1 + PKCE, rate limiting, security headers

**Performance:** Redis caching (90% DB load reduction), database indexing (30% I/O reduction), CDN (50%+ latency cut), connection pooling

**Testing:** 70-20-10 pyramid (unit-integration-E2E), Vitest 50% faster than Jest, contract testing for microservices, 83% migrations fail without tests

**DevOps:** Blue-green/canary deployments, feature flags (90% fewer failures), Kubernetes 84% adoption, Prometheus/Grafana monitoring, OpenTelemetry tracing

---

---

## Reference Navigation

**Core Technologies:**
- `backend-technologies.md` - Languages, frameworks, databases, message queues, ORMs
- `backend-api-design.md` - REST, GraphQL, gRPC patterns and best practices

**Security & Authentication:**
- `backend-security.md` - OWASP Top 10 2025, security best practices, input validation
- `backend-authentication.md` - OAuth 2.1, JWT, RBAC, MFA, session management

**Performance & Architecture:**
- `backend-performance.md` - Caching, query optimization, load balancing, scaling
- `backend-architecture.md` - Microservices, event-driven, CQRS, saga patterns

**Quality & Operations:**
- `backend-testing.md` - Testing strategies, frameworks, tools, CI/CD testing
- `backend-code-quality.md` - SOLID principles, design patterns, clean code
- `backend-devops.md` - Docker, Kubernetes, deployment strategies, monitoring
- `backend-debugging.md` - Debugging strategies, profiling, logging, production debugging

**Mindset & Collaboration:**
- `backend-mindset.md` - Problem-solving, architectural thinking, collaboration

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OAuth 2.1: https://oauth.net/2.1/
- OpenTelemetry: https://opentelemetry.io/
- Detailed references: [`references/`](references/) directory (backend-technologies.md, backend-api-design.md, backend-security.md, backend-authentication.md, backend-performance.md, backend-architecture.md, backend-testing.md, backend-code-quality.md, backend-devops.md, backend-debugging.md, backend-mindset.md)

---

## Triggers

Use this skill when:
- "implement a backend API"
- "create a REST endpoint"
- "build a Node.js service"
- "implement GraphQL resolver"
- "create a microservice"
- "build authentication system"
- "implement database operations"
- "create backend with clean architecture"
- "production-ready backend implementation"

Do NOT use for frontend code, simple scripts, or when the task explicitly requires a specific framework's patterns beyond TypeScript/Node.js.

---

## Process

### Phase 0: Check Existing Documentation (MANDATORY)

Before writing any code, ALWAYS check for existing project documentation:

**0.1 Check `/docs` folder for existing task documentation:**
```bash
# List all task folders sorted by date
ls -la /docs/YYYY_MM_DD_*/

# Read relevant task docs if they exist
/docs/YYYY_MM_DD_<relevant-task>/original_tasks.md
/docs/YYYY_MM_DD_<relevant-task>/analysis_result.md
/docs/YYYY_MM_DD_<relevant-task>/implementation_plan.md
```

**0.2 Check project-level documentation:**
```bash
# Common locations for project docs
./README.md
./ARCHITECTURE.md
./DECISIONS.md
./docs/**/*.md
```

**0.3 Review existing conventions from previous phases:**

When previous task phases exist (Phase 1, 2, etc.), read and respect:
- **Technology choices** already made (framework, ORM, auth strategy)
- **Architecture decisions** already documented in DECISIONS.md
- **Folder structure conventions** already established
- **Coding standards** from implementation_plan.md
- **Error handling patterns** already implemented

**0.4 If conflicts found:**

If existing documentation specifies different approaches than this skill suggests:
1. **Respect existing decisions** — Documented decisions take precedence over skill defaults
2. **Flag inconsistencies** — Note in implementation_report.md if you found conflicts
3. **Propose improvements** — If existing patterns have issues, document them in DECISIONS.md as new ADRs

**Decision priority:**
```
1. existing DECISIONS.md (authoritative)  ← highest priority
2. existing implementation_plan.md
3. existing analysis_result.md
4. skill defaults (backend-execution SKILL.md)
```

### Phase 1: Architecture & Structure Planning

Before writing code, establish the architectural foundation:

**1.1 Define Layered Architecture:**

```
src/
├── controllers/          # HTTP layer (express/fastify handlers)
├── services/             # Business logic (pure functions)
├── repositories/         # Data access layer (DB queries)
├── models/              # Domain entities & types
├── middleware/           # Express middleware (auth, validation, logging)
├── routes/               # Route definitions
├── config/               # Configuration (env, constants)
├── utils/               # Shared utilities
├── errors/              # Custom error classes
├── validators/          # Input validation schemas
└── __tests__/           # Unit/integration tests
```

**1.2 Define Error Architecture:**

```typescript
// errors/AppError.ts
export class AppError extends Error {
  constructor(
    public code: string,           // Machine-readable: 'USER_NOT_FOUND'
    public message: string,        // Human-readable
    public statusCode: number = 500,
    public isOperational: boolean = true  // true = expected error, false = bug
  ) {
    super(message);
  }
}

// errors/ErrorCodes.ts
export const ErrorCodes = {
  VALIDATION_ERROR: { code: 'VALIDATION_ERROR', statusCode: 400 },
  UNAUTHORIZED: { code: 'UNAUTHORIZED', statusCode: 401 },
  FORBIDDEN: { code: 'FORBIDDEN', statusCode: 403 },
  NOT_FOUND: { code: 'NOT_FOUND', statusCode: 404 },
  CONFLICT: { code: 'CONFLICT', statusCode: 409 },
  INTERNAL_ERROR: { code: 'INTERNAL_ERROR', statusCode: 500 },
} as const;
```

### Phase 2: Security Hardening

**2.1 Input Validation (MANDATORY):**

```typescript
// Use Zod for schema validation - NEVER trust raw request body
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase')
    .regex(/[a-z]/, 'Password must contain lowercase')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string().min(2).max(100),
  role: z.enum(['user', 'admin']).default('user'),
});

// Validate in controller, NOT in service
export async function createUser(req: Request, res: Response) {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ error: result.error.flatten() });
  }
  // Proceed with result.data (type-safe, validated)
}
```

**2.2 SQL Injection Prevention:**

```typescript
// ❌ NEVER use template literals with user input in queries
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Use parameterized queries (Prisma, TypeORM, Knex)
const user = await prisma.user.findUnique({ where: { id: userId } });

// ✅ If raw SQL needed, use parameterized values
const result = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
);
```

**2.3 Authentication & Authorization:**

```typescript
// middleware/auth.ts
export function authenticate(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'UNAUTHORIZED' });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = payload;  // TypeScript: extend Express Request
    next();
  } catch {
    return res.status(401).json({ error: 'INVALID_TOKEN' });
  }
}

// Role-based authorization
export function authorize(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'FORBIDDEN' });
    }
    next();
  };
}

// Usage in routes
router.post('/users', authenticate, authorize('admin'), createUser);
```

**2.4 Rate Limiting:**

```typescript
import rateLimit from 'express-rate-limit';

// Global rate limit
export const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // 100 requests per window
  message: { error: 'TOO_MANY_REQUESTS' },
  standardHeaders: true,
  legacyHeaders: false,
});

// Auth-specific (stricter)
export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,                      // 5 attempts
  message: { error: 'TOO_MANY_AUTH_ATTEMPTS' },
});
```

**2.5 Security Headers:**

```typescript
// middleware/security.ts
import helmet from 'helmet';

export const securityHeaders = helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
});
```

### Phase 3: Error Handling & Logging

**3.1 Structured Error Handler Middleware:**

```typescript
// middleware/errorHandler.ts
export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error with correlation ID
  logger.error({
    correlationId: req.correlationId,
    path: req.path,
    method: req.method,
    error: {
      message: err.message,
      stack: err.stack,
      code: err instanceof AppError ? err.code : 'INTERNAL_ERROR',
    },
  });

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.code,
      message: err.message,
      correlationId: req.correlationId,
    });
  }

  // Unknown errors: don't leak details in production
  return res.status(500).json({
    error: 'INTERNAL_ERROR',
    message: process.env.NODE_ENV === 'development' ? err.message : 'An unexpected error occurred',
    correlationId: req.correlationId,
  });
};
```

**3.2 Correlation ID Middleware:**

```typescript
// middleware/correlationId.ts
import { randomUUID } from 'crypto';

export function correlationId(req: Request, res: Response, next: NextFunction) {
  const id = (req.headers['x-correlation-id'] as string) || randomUUID();
  req.correlationId = id;
  res.setHeader('x-correlation-id', id);
  next();
}

// Extend Express Request
declare global {
  namespace Express {
    interface Request {
      correlationId: string;
      user?: { id: string; role: string };
    }
  }
}
```

**3.3 Async Error Wrapper:**

```typescript
// utils/asyncHandler.ts
export const asyncHandler = (fn: (req: Request, res: Response, next: NextFunction) => Promise<any>) =>
  (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };

// Usage: eliminates try/catch in every controller
router.post('/users', asyncHandler(async (req, res) => {
  const user = await userService.create(req.body);
  res.status(201).json(user);
}));
```

### Phase 3: Error Handling & Database Logging

**NOTE:** Error logging with persistent database storage is MANDATORY and defined in coder-execution agent (STEP 3).
The coder-execution agent enforces: every catch block must write to a persistent error log (database table), not just console.

Key patterns from coder-execution:
- Every `catch` block → write to `ErrorLog` table (timestamp, level, source, message, stack_trace, context, correlation_id)
- Correlation ID middleware for end-to-end tracing
- Structured JSON logging (queryable, not free text)
- No PII in logs (log reference IDs, not personal data)

This skill (backend-execution) focuses on architecture patterns. See [`references/backend-debugging.md`](references/backend-debugging.md) for detailed logging strategies.

### Phase 4: Repository Pattern (Data Access)

**4.1 Repository Interface:**

```typescript
// repositories/IUserRepository.ts
export interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
  update(id: string, data: UpdateUserDTO): Promise<User>;
  delete(id: string): Promise<void>;
}
```

**4.2 Prisma Implementation:**

```typescript
// repositories/PrismaUserRepository.ts
export class PrismaUserRepository implements IUserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }

  async create(data: CreateUserDTO): Promise<User> {
    // Hash password in service, not here
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserDTO): Promise<User> {
    return this.prisma.user.update({ where: { id }, data });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }
}
```

### Phase 5: Service Layer (Business Logic)

**5.1 Service with Dependency Injection:**

```typescript
// services/UserService.ts
export class UserService {
  constructor(
    private userRepo: IUserRepository,
    private eventEmitter: EventEmitter,
  ) {}

  async createUser(data: CreateUserDTO): Promise<User> {
    // Check for duplicate
    const existing = await this.userRepo.findByEmail(data.email);
    if (existing) {
      throw new AppError('EMAIL_EXISTS', 'Email already registered', 409);
    }

    // Hash password with bcrypt/argon2
    const hashedPassword = await argon2.hash(data.password);

    // Create user
    const user = await this.userRepo.create({
      ...data,
      password: hashedPassword,
    });

    // Emit domain event
    this.eventEmitter.emit('user.created', { userId: user.id, email: user.email });

    return user;
  }

  async getUserById(id: string): Promise<User> {
    const user = await this.userRepo.findById(id);
    if (!user) {
      throw new AppError('USER_NOT_FOUND', 'User not found', 404);
    }
    return user;
  }
}
```

### Phase 6: Performance Optimization

**6.1 Database Indexing:**

```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status) WHERE status IN ('pending', 'processing');
```

**6.2 Query Optimization:**

```typescript
// ❌ N+1 query problem
const orders = await prisma.order.findMany();
const users = orders.map(order => await prisma.user.findUnique({ where: { id: order.userId } }));

// ✅ Eager loading with include
const orders = await prisma.order.findMany({
  include: { user: true },  // Single query with JOIN
});

// ✅ Selective fields when full entity not needed
const userEmails = await prisma.user.findMany({
  select: { email: true },
});
```

**6.3 Caching Strategy:**

```typescript
import { Redis } from 'ioredis';

export class CacheService {
  constructor(private redis: Redis) {}

  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: any, ttlSeconds = 300): Promise<void> {
    await this.redis.setex(key, ttlSeconds, JSON.stringify(value));
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length) await this.redis.del(...keys);
  }
}
```

---

## Required Output Documentation

**NOTE:** Output documentation requirements (ARCHITECTURE.md, .env.example, DECISIONS.md, implementation_report.md) are defined in coder-execution agent. This skill focuses on architecture patterns.

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Ignoring existing architecture decisions | Check `/docs` folder first; respect documented ADRs |
| Overwriting existing conventions | Follow established folder structure and patterns from previous phases |
| Creating duplicate documentation | Update existing ARCHITECTURE.md/DECISIONS.md instead of creating new ones |
| Raw `req.body` in services | Validate with Zod/Joi, pass typed DTO |
| Template literals in SQL | Parameterized queries or ORM |
| Console.log for errors | Structured logging with correlation ID |
| Singleton repositories | Dependency injection for testability |
| Synchronous code in handlers | Async/await with proper error wrapping |
| Hardcoded secrets | Environment variables with validation |
| Missing database indexes | Analyze queries and add appropriate indexes |
| N+1 queries | Eager loading with `include` or `join` |
| No rate limiting | Implement rate limiters per endpoint sensitivity |
| Storing passwords in plain text | bcrypt/argon2 with proper rounds |

---

## Execution Checklist

**NOTE:** Error logging with persistence is MANDATORY and handled by coder-execution agent. This checklist focuses on architecture patterns.

```
[ ] Phase 0: Check /docs folder for existing task documentation
[ ] Phase 0: Review existing architecture decisions (DECISIONS.md, implementation_plan.md)
[ ] Phase 0: Note any conflicts between existing conventions and skill defaults
[ ] Phase 1: Define project structure and layer architecture (respect existing conventions)
[ ] Phase 2: Implement input validation schemas (Zod)
[ ] Phase 2: Add authentication middleware (JWT verification)
[ ] Phase 2: Configure rate limiting (global + sensitive endpoints)
[ ] Phase 2: Add security headers (helmet)
[ ] Phase 4: Define repository interfaces
[ ] Phase 4: Implement repository with Prisma/ORM
[ ] Phase 5: Create service layer with dependency injection
[ ] Phase 6: Add database indexes for frequent queries
[ ] Phase 6: Implement caching for expensive operations
[ ] Verify: All user inputs are validated
[ ] Verify: Passwords are hashed with bcrypt/argon2
[ ] Verify: Rate limiting is configured
[ ] Verify: Respected existing architecture decisions from /docs
[ ] Verify: Technology stack matches existing project (no silent introduction of new tech)
```

---

## Verification

After backend implementation:
1. ✅ Checked `/docs` folder for existing task documentation before starting
2. ✅ Respected existing architecture decisions and conventions
3. ✅ Used existing technology stack (no new tech without user approval)
4. ✅ Input validation rejects invalid data with 400 status and details
5. ✅ Authentication middleware returns 401 for missing/invalid tokens
6. ✅ Rate limiting returns 429 after threshold exceeded
7. ✅ Passwords stored are hashed (never plain text)
8. ✅ SQL queries use parameterized statements (no injection possible)
9. ✅ `.env.example` contains all required environment variables
10. ✅ `ARCHITECTURE.md` documents folder structure and layer dependencies (or updated existing)
11. ✅ `DECISIONS.md` explains key architectural choices (or updated existing)

**Error logging verification (handled by coder-execution agent):**
- ✅ Every catch block writes to persistent error log (database table)
- ✅ Correlation ID present for end-to-end tracing
- ✅ No PII in logs
