# Backend Testing Strategies

## Testing Pyramid

```
        ╱╲
       ╱  ╲
      ╱ E2E╲        10% - Few, slow, high confidence
     ╱──────╲
    ╱        ╲
   ╱Integration╲   20% - Service boundaries, DB
  ╱────────────╲
 ╱              ╲
╱    Unit        ╲  70% - Fast, isolated, many
╲────────────────╱
```

## Unit Testing

```typescript
// Example: UserService unit test
import { describe, it, expect, vi } from 'vitest';
import { UserService } from './UserService';
import { AppError } from '../errors/AppError';

describe('UserService', () => {
  const mockUserRepo = {
    findByEmail: vi.fn(),
    create: vi.fn(),
  };

  const userService = new UserService(mockUserRepo);

  describe('createUser', () => {
    it('should throw EMAIL_EXISTS if email already registered', async () => {
      mockUserRepo.findByEmail.mockResolvedValue({ id: '1', email: 'test@test.com' });

      await expect(
        userService.createUser({ email: 'test@test.com', password: 'password123' })
      ).rejects.toThrow(AppError);

      expect(mockUserRepo.findByEmail).toHaveBeenCalledWith('test@test.com');
    });

    it('should create user with hashed password', async () => {
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.create.mockImplementation((data) =>
        Promise.resolve({ id: '1', ...data, password: 'hashed' })
      );

      const result = await userService.createUser({
        email: 'test@test.com',
        password: 'password123',
      });

      expect(result.password).not.toBe('password123'); // Password should be hashed
      expect(mockUserRepo.create).toHaveBeenCalledWith(
        expect.objectContaining({
          email: 'test@test.com',
        })
      );
    });
  });
});
```

## Integration Testing

```typescript
// Example: API integration test with Supertest
import request from 'supertest';
import { app } from '../app';
import { prisma } from '../database/prisma';

describe('POST /api/v1/users', () => {
  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  it('should create a new user', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({
        email: 'test@example.com',
        password: 'Password123!',
        name: 'Test User',
      })
      .expect(201);

    expect(response.body.data).toMatchObject({
      email: 'test@example.com',
      name: 'Test User',
    });
    expect(response.body.data.password).toBeUndefined(); // Password should not be returned
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({
        email: 'invalid-email',
        password: 'Password123!',
        name: 'Test User',
      })
      .expect(400);

    expect(response.body.error).toBe('VALIDATION_ERROR');
  });
});
```

## E2E Testing

```typescript
// Example: Playwright E2E test
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test('should register, login, and access protected route', async ({ page }) => {
    // Register
    await page.goto('/register');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'Password123!');
    await page.fill('[name="name"]', 'Test User');
    await page.click('[type="submit"]');

    // Should redirect to login
    await expect(page).toHaveURL('/login');

    // Login
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'Password123!');
    await page.click('[type="submit"]');

    // Should be on dashboard
    await expect(page).toHaveURL('/dashboard');

    // Access protected resource
    await page.goto('/api/v1/protected');
    const response = await page.request.get('/api/v1/protected');
    expect(response.status()).toBe(200);
  });
});
```

## Contract Testing (Microservices)

```typescript
// Provider side (service being tested)
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      email: 'test@example.com',
      name: 'Test User',
    });
  })
);

test('User API contract', async () => {
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json({
        id: '123',
        email: 'test@example.com',
        // Missing 'name' - contract violation
      });
    })
  );

  const response = await fetch('/api/users/123');
  const data = await response.json();

  // This will fail if consumer expects 'name' but provider doesn't return it
  expect(data).toMatchSchema({
    type: 'object',
    required: ['id', 'email', 'name'],
  });
});
```

## Database Testing

```typescript
// Testcontainers for PostgreSQL
import { PostgreSqlContainer } from '@testcontainers/postgresql';
import { PrismaClient } from '@prisma/client';

describe('User Repository', () => {
  let container: PostgreSqlContainer;
  let prisma: PrismaClient;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    prisma = new PrismaClient({
      datasources: { db: { url: container.getConnectionUri() } },
    });
  });

  afterAll(async () => {
    await prisma.$disconnect();
    await container.stop();
  });

  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  it('should create and retrieve a user', async () => {
    const created = await prisma.user.create({
      data: { email: 'test@example.com', name: 'Test', passwordHash: 'hash' },
    });

    const found = await prisma.user.findUnique({
      where: { id: created.id },
    });

    expect(found?.email).toBe('test@example.com');
  });
});
```

## Load Testing

```typescript
// k6 load test
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% failure rate
  },
};

export default function () {
  const res = http.get('http://localhost:3000/api/v1/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'has products': (r) => JSON.parse(r.body).data.length > 0,
  });
  sleep(1);
}
```

## Test Coverage

```bash
# vitest coverage
npx vitest run --coverage

# nyc for Istanbul coverage
npx nyc --reporter=text mocha tests/**/*.ts
```

## Mocking Patterns

```typescript
// HTTP mocking with msw
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

export const server = setupServer(
  http.get('https://api.external.com/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'John' },
    ]);
  })
);

// Use in tests
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Testing Checklist

- [ ] Unit tests for all service methods (business logic)
- [ ] Integration tests for all API endpoints
- [ ] Database tests with real/test database
- [ ] Authentication/authorization tests
- [ ] Error handling tests (4xx, 5xx responses)
- [ ] Validation tests (invalid inputs)
- [ ] E2E tests for critical user flows
- [ ] Load tests for performance-critical endpoints
- [ ] Contract tests for microservice boundaries
- [ ] Security tests (SQL injection, XSS, auth bypass)