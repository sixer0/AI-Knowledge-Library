---
name: gsp-frontend-integration
version: 1.0.1
description: >-
  Production-grade frontend-backend integration skill. Connects UI components
  to real backend API endpoints with proper error handling, loading states,
  and end-to-end verification. CRITICAL: All integrations MUST be tested
  against actual running backend — never assume endpoints exist or work.
  Use when implementing frontend features that call backend APIs.
license: MIT
metadata:
  hermes:
    tags: [gsp, development]
    category: development
  category: development
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/frontend-integration
---

# Frontend Integration Skill

Production-grade frontend-backend integration with real endpoint testing and robust error handling.

---


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Berlaku atas **artefak tulis** skill ini (README, komentar/docstring, changelog, laporan review, spesifikasi API); kaidah pemrograman tidak diubah.
Kontrak keluaran seragam: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) **Module L** - L.2 header-metadata (`title,date,author_profile,status,task_ref,source_refs`),
L.3 heading bernomor + berkas `snake_case` (dokumen DATUM TERBIT/SERAH ikut DT-12), L.4 angka wajib `[R-n, sumber, hal]`, L.5 bahasa mengikuti user, L.6 checklist pra-serah (Module F.1) sebelum menyerahkan.
Konflik FORMAT → Module L menang; konflik GAYA presisi → Module H/K tetap menang.
## Triggers

Use this skill when:
- "integrate frontend with backend API"
- "connect UI to REST endpoints"
- "implement API call in frontend"
- "add data fetching to component"
- "hook up form to backend"
- "integrate GraphQL resolver"
- "test API integration end-to-end"
- "implement webhook frontend handler"

Do NOT use for:
- Pure frontend design (use `frontend-design` skill)
- Backend-only implementation (use `backend-execution` skill)
- Static content without API calls
- Mocked data without real endpoint testing

---

## Critical Rule: Test Against Real Backend

**NEVER assume an endpoint exists or works.** Every integration MUST be verified against the actual running backend before delivery.

```
❌ WRONG: Write code assuming /api/users works
✅ RIGHT: Test /api/users first, then write code based on actual response
```

---

## Process

### Phase 0: Check Existing Documentation (MANDATORY)

Before writing any integration code, check for existing documentation:

**0.1 Check `/docs` folder for project documentation:**
```bash
ls -la /docs/YYYY_MM_DD_*/
cat /docs/YYYY_MM_DD_<task>/implementation_plan.md
cat /docs/YYYY_MM_DD_<task>/analysis_result.md
```

**0.2 Identify REAL backend endpoints:**

From existing documentation or by inspecting the backend codebase:
```bash
# Find route definitions
grep -r "Router\|@Controller\|route\|Router.post\|Router.get" --include="*.ts" backend/src/

# Find API prefix
grep -r "API_PREFIX\|baseURL\|/api" --include="*.ts" backend/src/
```

**0.3 Verify backend is running:**
```bash
# Check if backend is accessible
curl -s http://localhost:3000/api/health || echo "Backend not running"

# If not running, do NOT proceed with integration
# Document: "Backend not available - integration blocked"
```

---

### Phase 0.5: Swagger / OpenAPI Discovery (MANDATORY)

Before integrating, check if backend provides API documentation:

**0.5.1 Detect Swagger/OpenAPI:**
```bash
# Common Swagger endpoints
curl -s http://localhost:3000/api/docs 2>/dev/null | head -20
curl -s http://localhost:3000/swagger-ui.html 2>/dev/null | head -20
curl -s http://localhost:3000/api/openapi.json 2>/dev/null | jq '.paths | keys'
curl -s http://localhost:3000/api/swagger.json 2>/dev/null | jq '.'

# Alternative paths
curl -s http://localhost:3000/docs.json 2>/dev/null
curl -s http://localhost:3000/api/api-docs 2>/dev/null
```

**0.5.2 Parse OpenAPI spec for needed endpoints:**

If `openapi.json` is available, extract the endpoints you need:

```bash
# Get all paths from OpenAPI spec
curl -s http://localhost:3000/api/openapi.json | jq '.paths | keys[]'

# Get specific endpoint details
curl -s http://localhost:3000/api/openapi.json | jq '.paths["/api/users"]'

# Get request/response schemas
curl -s http://localhost:3000/api/openapi.json | jq '.components.schemas.User'
```

**0.5.3 Document discovered vs needed endpoints:**

```markdown
## Endpoint Discovery Report

### Swagger/OpenAPI Found
- URL: http://localhost:3000/api/openapi.json
- Status: ✅ Found / ❌ Not Found

### Available Endpoints (from Swagger)
| Method | Path | Summary |
|--------|------|---------|
| GET | /api/users | Get all users |
| POST | /api/users | Create user |
| GET | /api/users/{id} | Get user by ID |

### Needed Endpoints (for frontend)
| Method | Path | Purpose | Status |
|--------|------|---------|--------|
| GET | /api/users | User list | ✅ Exists |
| POST | /api/users | Create user | ✅ Exists |
| DELETE | /api/users/{id} | Delete user | ❌ MISSING |
| GET | /api/users/{id}/orders | User orders | ❌ MISSING |

### Missing Endpoints (Requires Backend Implementation)
| Method | Path | Purpose | Priority |
|--------|------|---------|----------|
| DELETE | /api/users/{id} | Delete user | HIGH |
| GET | /api/users/{id}/orders | User orders | MEDIUM |
```

---

### Phase 0.6: Handle Missing Endpoints

**When an endpoint doesn't exist, you MUST either:**

**Option A: Report & Request (PREFERRED for missing features)**
```markdown
## 🚨 MISSING ENDPOINT REPORT

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Reporter:** frontend-integration skill

### Missing Endpoints

| Method | Path | Purpose | Priority | Status |
|--------|------|---------|----------|--------|
| DELETE | /api/users/{id} | Delete user | HIGH | REPORTED |
| GET | /api/users/{id}/orders | User orders | MEDIUM | REPORTED |

### Backend Implementation Needed

For frontend to complete user management feature, the following endpoints are required:

#### DELETE /api/users/{id}
**Purpose:** Delete a user by ID
**Priority:** HIGH
**Suggested Response:**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```
**Error Responses:**
- 404: User not found
- 401: Unauthorized
- 403: Forbidden (non-admin)

#### GET /api/users/{id}/orders
**Purpose:** Get all orders for a specific user
**Priority:** MEDIUM
**Suggested Response:**
```json
{
  "orders": [
    {
      "id": "ord_xxx",
      "userId": "usr_xxx",
      "status": "pending",
      "total": 99.99,
      "createdAt": "2026-06-16T00:00:00.000Z"
    }
  ],
  "total": 1
}
```
**Error Responses:**
- 404: User not found
- 401: Unauthorized

### Action Required

Please implement these endpoints in the backend before frontend integration can be completed.

---
*Reported: YYYY-MM-DD HH:mm*
```

**Option B: Implement Missing Endpoint (if authorized)**
If you have `backend-execution` skill authorization and the missing endpoint is simple:
1. Load `backend-execution` skill
2. Implement the missing endpoint
3. Document in integration report
4. Continue with frontend integration

**0.6.1 Document missing endpoint in task:**
```bash
# Update task status
echo "MISSING_ENDPOINTS: DELETE /api/users/{id}, GET /api/users/{id}/orders" >> /docs/YYYY_MM_DD_<task>/issues.md
```

---

### Phase 1: Endpoint Discovery & Contract

**1.1 Document the API contract:**

For each endpoint you need to integrate with, create an API contract:

```typescript
// api/contracts/users.contract.ts

/**
 * GET /api/users
 * Retrieves list of users
 *
 * Real response verified: 2026-06-16
 * Backend: http://localhost:3000
 */
export interface UserListResponse {
  users: Array<{
    id: string;
    email: string;
    name: string;
    role: 'admin' | 'user';
    createdAt: string;  // ISO date
  }>;
  total: number;
  page: number;
  pageSize: number;
}

/**
 * POST /api/users
 * Creates a new user
 *
 * Request body verified: 2026-06-16
 */
export interface CreateUserRequest {
  email: string;
  password: string;
  name: string;
  role?: 'admin' | 'user';
}

export interface CreateUserResponse {
  user: User;
  message: string;
}
```

**1.2 Test the actual endpoint:**

```bash
# GET endpoint
curl -s http://localhost:3000/api/users | jq .

# POST endpoint
curl -s -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test1234","name":"Test"}' | jq .

# Check response status and structure
curl -s -w "\nHTTP_STATUS:%{http_code}" http://localhost:3000/api/users
```

**1.3 Document actual response:**

```markdown
# API Contract: GET /api/users

**Verified:** 2026-06-16
**Status:** 200 OK

**Response:**
```json
{
  "users": [...],
  "total": 10,
  "page": 1,
  "pageSize": 20
}
```

**Error cases:**
- 401 Unauthorized: Missing or invalid token
- 403 Forbidden: Insufficient permissions
- 500 Internal Server Error: Server error
```

---

### Phase 2: API Client Implementation

**2.1 Create typed API client:**

```typescript
// api/client.ts
import type { UserListResponse, CreateUserRequest, CreateUserResponse } from './contracts/users.contract';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';

class ApiClient {
  private baseUrl: string;
  private defaultHeaders: HeadersInit;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    const headers: HeadersInit = {
      ...this.defaultHeaders,
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      // Parse error response
      let errorMessage = `HTTP ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorData.error || errorMessage;
      } catch {
        // Response body not JSON
      }

      throw new ApiError({
        status: response.status,
        message: errorMessage,
        endpoint,
        method: options.method || 'GET',
      });
    }

    return response.json();
  }

  // User endpoints
  async getUsers(page = 1, pageSize = 20): Promise<UserListResponse> {
    return this.request<UserListResponse>(
      `/api/users?page=${page}&pageSize=${pageSize}`
    );
  }

  async createUser(data: CreateUserRequest): Promise<CreateUserResponse> {
    return this.request<CreateUserResponse>('/api/users', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getUser(id: string): Promise<User> {
    return this.request<User>(`/api/users/${id}`);
  }

  async updateUser(id: string, data: Partial<CreateUserRequest>): Promise<User> {
    return this.request<User>(`/api/users/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async deleteUser(id: string): Promise<void> {
    return this.request<void>(`/api/users/${id}`, {
      method: 'DELETE',
    });
  }
}

export class ApiError extends Error {
  constructor(public payload: {
    status: number;
    message: string;
    endpoint: string;
    method: string;
  }) {
    super(payload.message);
    this.name = 'ApiError';
  }
}

// Singleton instance
export const apiClient = new ApiClient();
```

---

### Phase 3: React Integration Patterns

**3.1 Data Fetching Hook:**

```typescript
// hooks/useUsers.ts
import { useState, useEffect, useCallback } from 'react';
import { apiClient, ApiError } from '@/api/client';

interface UseUsersOptions {
  page?: number;
  pageSize?: number;
  enabled?: boolean;
}

interface UseUsersResult {
  users: User[] | null;
  total: number;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useUsers(options: UseUsersOptions = {}): UseUsersResult {
  const { page = 1, pageSize = 20, enabled = true } = options;

  const [users, setUsers] = useState<User[] | null>(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async () => {
    if (!enabled) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.getUsers(page, pageSize);
      setUsers(response.users);
      setTotal(response.total);
    } catch (err) {
      const message = err instanceof ApiError
        ? err.payload.message
        : 'Failed to load users';
      setError(message);
      setUsers(null);
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, enabled]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return { users, total, loading, error, refetch: fetchUsers };
}
```

**3.2 Mutation Hook with Loading & Error:**

```typescript
// hooks/useCreateUser.ts
import { useState, useCallback } from 'react';
import { apiClient, ApiError } from '@/api/client';

interface UseCreateUserResult {
  createUser: (data: CreateUserRequest) => Promise<{ success: boolean; error?: string }>;
  loading: boolean;
  error: string | null;
}

export function useCreateUser(): UseCreateUserResult {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createUser = useCallback(async (data: CreateUserRequest) => {
    setLoading(true);
    setError(null);

    try {
      await apiClient.createUser(data);
      return { success: true };
    } catch (err) {
      const message = err instanceof ApiError
        ? err.payload.message
        : 'Failed to create user';
      setError(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  }, []);

  return { createUser, loading, error };
}
```

**3.3 Component with Full Error Handling:**

```tsx
// components/UserList.tsx
'use client';

import { useUsers } from '@/hooks/useUsers';
import { useCreateUser } from '@/hooks/useCreateUser';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Spinner } from '@/components/ui/Spinner';
import { ErrorState } from '@/components/ui/ErrorState';
import { EmptyState } from '@/components/ui/EmptyState';

export function UserList() {
  const { users, total, loading, error, refetch } = useUsers({ page: 1 });
  const { createUser, loading: creating } = useCreateUser();

  // Error state
  if (error && !users) {
    return (
      <ErrorState
        title="Failed to load users"
        message={error}
        onRetry={refetch}
      />
    );
  }

  // Loading state (initial)
  if (loading && !users) {
    return <Spinner />;
  }

  // Empty state
  if (!loading && users?.length === 0) {
    return (
      <EmptyState
        title="No users yet"
        description="Create your first user to get started."
        action={
          <Button onClick={() => openCreateModal()}>
            Create User
          </Button>
        }
      />
    );
  }

  return (
    <div className="space-y-4">
      {/* User list */}
      <div className="divide-y">
        {users?.map((user) => (
          <UserRow key={user.id} user={user} />
        ))}
      </div>

      {/* Pagination info */}
      <div className="text-sm text-muted">
        Showing {users?.length} of {total} users
      </div>
    </div>
  );
}
```

---

### Phase 4: End-to-End Testing (MANDATORY)

**4.1 Test Against Real Backend:**

```bash
# 1. Ensure backend is running
curl -s http://localhost:3000/api/health
# Must return: {"status":"ok","timestamp":"..."}

# 2. Test authentication (if required)
TOKEN=$(curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"Admin1234!"}' | jq -r '.token')

echo "Token: $TOKEN"

# 3. Test each endpoint with real data
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/users | jq '.'

# 4. Test error cases
# 401 - no token
curl -s http://localhost:3000/api/users

# 400 - invalid data
curl -s -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"invalid"}' | jq '.'
```

**4.2 Integration Test File:**

```typescript
// __tests__/api/users.integration.test.ts
/**
 * Integration tests - require real backend running at localhost:3000
 * Run: npm run test:integration
 */

describe('User API Integration', () => {
  const BASE_URL = process.env.TEST_API_URL || 'http://localhost:3000';
  let authToken: string;

  beforeAll(async () => {
    // Login to get token
    const loginRes = await fetch(`${BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'admin@test.com',
        password: 'Admin1234!',
      }),
    });

    if (!loginRes.ok) {
      throw new Error('Failed to authenticate - is the backend running?');
    }

    const loginData = await loginRes.json();
    authToken = loginData.token;
  });

  describe('GET /api/users', () => {
    it('should return users list with valid token', async () => {
      const res = await fetch(`${BASE_URL}/api/users`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(res.ok).toBe(true);
      const data = await res.json();
      expect(data.users).toBeDefined();
      expect(Array.isArray(data.users)).toBe(true);
    });

    it('should return 401 without token', async () => {
      const res = await fetch(`${BASE_URL}/api/users`);
      expect(res.status).toBe(401);
    });
  });

  describe('POST /api/users', () => {
    const testEmail = `test-${Date.now()}@test.com`;

    it('should create user with valid data', async () => {
      const res = await fetch(`${BASE_URL}/api/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify({
          email: testEmail,
          password: 'Test1234!',
          name: 'Test User',
        }),
      });

      expect(res.status).toBe(201);
      const data = await res.json();
      expect(data.user.email).toBe(testEmail);
    });

    it('should return 400 for invalid email', async () => {
      const res = await fetch(`${BASE_URL}/api/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authToken}`,
        },
        body: JSON.stringify({
          email: 'invalid-email',
          password: 'Test1234!',
          name: 'Test',
        }),
      });

      expect(res.status).toBe(400);
    });
  });
});
```

**4.3 Playwright E2E Test:**

```typescript
// e2e/users.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('[name="email"]', 'admin@test.com');
    await page.fill('[name="password"]', 'Admin1234!');
    await page.click('[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
  });

  test('should display users list', async ({ page }) => {
    await page.goto('/users');

    // Wait for loading to finish
    await page.waitForSelector('[data-testid="user-list"]', { timeout: 5000 });

    // Should show users
    const rows = await page.locator('[data-testid="user-row"]').count();
    expect(rows).toBeGreaterThan(0);
  });

  test('should show error when API fails', async ({ page }) => {
    // Mock API failure
    await page.route('**/api/users', route => {
      route.fulfill({ status: 500, body: { error: 'SERVER_ERROR' } });
    });

    await page.goto('/users');

    // Should show error state
    await expect(page.getByText('Failed to load users')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Retry' })).toBeVisible();
  });

  test('should create user successfully', async ({ page }) => {
    await page.goto('/users');

    // Click create button
    await page.click('[data-testid="create-user-btn"]');

    // Fill form
    await page.fill('[name="email"]', `newuser-${Date.now()}@test.com`);
    await page.fill('[name="password"]', 'NewUser123!');
    await page.fill('[name="name"]', 'New User');

    // Submit
    await page.click('[type="submit"]');

    // Should show success
    await expect(page.getByText('User created successfully')).toBeVisible();
  });
});
```

---

## Required Output Documentation

Every frontend integration implementation MUST produce these documents:

### 1. API Contract Definitions (`api/contracts/*.ts`)

For each integrated endpoint, create a TypeScript contract file:

```typescript
// api/contracts/users.contract.ts

/**
 * User entity
 * Verified from: GET /api/users response
 */
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
  createdAt: string;  // ISO date
}

/**
 * GET /api/users - User list response
 * Verified: 2026-06-16 via curl
 * Status: 200 OK
 */
export interface UserListResponse {
  users: User[];
  total: number;
  page: number;
  pageSize: number;
}

/**
 * POST /api/users - Create user request
 * Verified: 2026-06-16 via curl
 */
export interface CreateUserRequest {
  email: string;
  password: string;
  name: string;
  role?: 'admin' | 'user';
}

/**
 * POST /api/users - Create user response
 * Verified: 2026-06-16 via curl
 * Status: 201 Created
 */
export interface CreateUserResponse {
  user: User;
  message: string;
}

/**
 * Error response format (all endpoints)
 * Verified: 2026-06-16 via curl
 */
export interface ApiErrorResponse {
  error: string;      // Machine-readable error code
  message: string;    // Human-readable message
  correlationId?: string;  // For debugging
}
```

### 2. Integration Report (`integration-report.md`)

```markdown
# Frontend-Backend Integration Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD
**Backend URL:** http://localhost:3000
**Frontend URL:** http://localhost:3001

---

## Executive Summary

[1-2 sentences describing what was integrated]

## Endpoint Inventory

### Authentication

| Method | Endpoint | Auth | Verified | Status |
|--------|----------|------|----------|--------|
| POST | /api/auth/login | No | ✅ | 200 OK |
| POST | /api/auth/refresh | Yes | ✅ | 200 OK |
| POST | /api/auth/logout | Yes | ✅ | 204 No Content |

### Users

| Method | Endpoint | Auth | Verified | Status |
|--------|----------|------|----------|--------|
| GET | /api/users | Yes | ✅ | 200 OK |
| GET | /api/users/:id | Yes | ✅ | 200 OK |
| POST | /api/users | Admin | ✅ | 201 Created |
| PATCH | /api/users/:id | Admin | ✅ | 200 OK |
| DELETE | /api/users/:id | Admin | ✅ | 204 No Content |

## Endpoint Details

### GET /api/users

**Verified:** 2026-06-16
**Auth Required:** Bearer token
**Request:**
```
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:3000/api/users?page=1&pageSize=20
```

**Success Response (200):**
```json
{
  "users": [
    {
      "id": "clx1234abcd",
      "email": "user@example.com",
      "name": "Test User",
      "role": "user",
      "createdAt": "2026-06-16T00:00:00.000Z"
    }
  ],
  "total": 1,
  "page": 1,
  "pageSize": 20
}
```

**Error Responses:**
| Status | Condition | Response |
|--------|-----------|----------|
| 401 | Missing/invalid token | `{"error":"UNAUTHORIZED","message":"Invalid token"}` |
| 403 | Insufficient permissions | `{"error":"FORBIDDEN","message":"Admin access required"}` |

### POST /api/users

**Verified:** 2026-06-16
**Auth Required:** Bearer token (admin)
**Request:**
```
curl -X POST http://localhost:3000/api/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"new@test.com","password":"Pass123!","name":"New User"}'
```

**Success Response (201):**
```json
{
  "user": { "id": "clx5678efgh", ... },
  "message": "User created successfully"
}
```

**Error Responses:**
| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Invalid input | `{"error":"VALIDATION_ERROR","message":"Invalid email format"}` |
| 409 | Email exists | `{"error":"CONFLICT","message":"Email already registered"}` |

---

## Integration Test Results

### curl Tests

| Test | Command | Expected | Actual | Status |
|------|---------|----------|--------|--------|
| Health check | `curl /api/health` | 200 | 200 | ✅ PASS |
| List users (auth) | `curl -H "Bearer $TOKEN" /api/users` | 200 | 200 | ✅ PASS |
| List users (no auth) | `curl /api/users` | 401 | 401 | ✅ PASS |
| Create user (valid) | `curl -X POST ...` | 201 | 201 | ✅ PASS |
| Create user (invalid) | `curl -X POST -d '{email:invalid}'` | 400 | 400 | ✅ PASS |

### Integration Tests (Jest)

```
Test Suites: 3 passed, 3 total
Tests:       12 passed, 12 total
```

### E2E Tests (Playwright)

```
Test Suites: 2 passed, 2 total
Tests:       8 passed, 8 total
```

---

## Error Handling Matrix

| Error Type | HTTP Status | User Message | Retry? | Logged? |
|------------|-------------|--------------|--------|---------|
| Network error | - | "Connection failed. Check your internet." | Yes (3x) | Yes |
| 400 Bad Request | 400 | [Field-specific validation message] | No | Yes |
| 401 Unauthorized | 401 | "Session expired. Please login again." | No | Yes |
| 403 Forbidden | 403 | "You don't have permission for this action." | No | Yes |
| 404 Not Found | 404 | "The requested resource was not found." | No | Yes |
| 409 Conflict | 409 | [Specific conflict message] | No | Yes |
| 500 Server Error | 500 | "Something went wrong. Please try again." | Yes (1x) | Yes |
| Network timeout | - | "Request timed out. Please try again." | Yes (3x) | Yes |

---

## Components & Hooks

### New Files Created

| File | Purpose |
|------|---------|
| `api/client.ts` | Typed API client with error handling |
| `api/contracts/users.contract.ts` | User API type definitions |
| `hooks/useUsers.ts` | User list data fetching hook |
| `hooks/useCreateUser.ts` | User creation mutation hook |
| `components/UserList.tsx` | User list component |
| `components/UserForm.tsx` | Create/edit user form |

### Modified Files

| File | Changes |
|------|---------|
| `app/users/page.tsx` | Added UserList component |
| `providers/QueryProvider.tsx` | Added React Query setup |

---

## State Management

### Loading States

| Component | State | UI |
|-----------|-------|-----|
| UserList | loading | Skeleton loader with 5 rows |
| UserForm | submitting | Button disabled + spinner |
| UserList | refetching | Subtle top spinner |

### Error States

| Component | Error | UI |
|-----------|-------|-----|
| UserList | failed to load | ErrorState with retry button |
| UserForm | failed to submit | Inline error message + toast |
| UserList | empty | EmptyState with create CTA |

---

## Environment Configuration

### .env.example

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_API_TIMEOUT=30000

# For production:
# NEXT_PUBLIC_API_URL=https://api.production.example.com
```

---

## Known Issues

| Issue | Severity | Status | Notes |
|-------|----------|--------|-------|
| None | - | - | All endpoints verified |

---

## Recommendations

- [Consider adding] React Query for automatic caching
- [Consider adding] SWR for data prefetching
- [Consider adding] Optimistic updates for better UX

---

*Generated: YYYY-MM-DD HH:mm*
*Backend verified against: http://localhost:3000*
```

### 3. Frontend Architecture (`FRONTEND_ARCH.md`)

```markdown
# Frontend Architecture

## Project Structure

```
src/
├── api/
│   ├── client.ts              # API client singleton
│   ├── contracts/             # TypeScript interfaces per domain
│   │   ├── users.contract.ts
│   │   └── ...
│   └── endpoints/             # Endpoint-specific helpers
│       └── users.ts
├── components/
│   ├── ui/                    # Base components (Button, Input, etc.)
│   ├── features/              # Feature-specific components
│   │   └── users/
│   │       ├── UserList.tsx
│   │       ├── UserForm.tsx
│   │       └── UserRow.tsx
│   └── layouts/
├── hooks/
│   ├── useUsers.ts
│   └── useCreateUser.ts
├── pages/                     # or app/ for Next.js
├── styles/
│   └── tokens.css             # Design tokens
└── utils/
    └── cn.ts                  # Class name utility
```

## API Layer Design

### Client Pattern

The API client (`api/client.ts`) is a singleton that:
1. Adds `Authorization: Bearer {token}` header when user is authenticated
2. Parses error responses into `ApiError` class
3. Handles `Content-Type: application/json` consistently
4. Returns typed responses based on contract interfaces

### Contract-Driven Development

All API responses are defined in `api/contracts/*.ts`:
- Source of truth is the **actual curl response**
- Interfaces are verified against real backend
- No assumed fields or types

## Error Handling Strategy

### Three-Layer Error Model

```
┌─────────────────────────────────────┐
│ Layer 1: User Feedback              │
│   Toast / Inline message            │
├─────────────────────────────────────┤
│ Layer 2: Client Logging             │
│   POST /api/logs/error              │
├─────────────────────────────────────┤
│ Layer 3: Graceful Degradation       │
│   Retry button / Fallback UI        │
└─────────────────────────────────────┘
```

### Retry Policy

| Error Type | Retry | Cooldown | Max Attempts |
|------------|-------|----------|--------------|
| Network timeout | Yes | 3s | 3 |
| 500 Server Error | Yes | 3s | 3 |
| 400/401/403/404 | No | - | 0 |
| 409 Conflict | No | - | 0 |

## Authentication Flow

```
1. User submits credentials
2. POST /api/auth/login
3. Store token in httpOnly cookie (secure)
4. API client reads token from cookie
5. All API requests include Authorization header
6. On 401: redirect to /login
```

## Performance Considerations

- React Query/SWR for caching and deduplication
- Optimistic updates for mutations
- Lazy loading for route-based code splitting
- Image optimization with next/image or similar

---

*Generated: YYYY-MM-DD*
```

### 4. Missing Endpoint Report (`MISSING_ENDPOINT_REPORT.md`)

*Create this ONLY if backend endpoints are missing*

```markdown
# 🚨 Missing Endpoint Report

**Project:** [Project Name]
**Date:** YYYY-MM-DD HH:mm
**Reporter:** frontend-integration skill
**Status:** PENDING BACKEND IMPLEMENTATION

---

## Summary

The following endpoints are required for frontend integration but do NOT exist in the backend.

**Frontend Feature Blocked:** [Feature name that can't be completed]

---

## Missing Endpoints

| Method | Path | Purpose | Priority | Suggested Status |
|--------|------|---------|----------|------------------|
| DELETE | /api/users/{id} | Delete user | HIGH | 204 No Content |
| GET | /api/users/{id}/orders | User orders | MEDIUM | 200 OK |

---

## Endpoint Specifications

### DELETE /api/users/{id}

**Purpose:** Delete a user account
**Priority:** HIGH
**Auth Required:** Yes (admin only)
**Path Parameters:**
| Name | Type | Description |
|------|------|-------------|
| id | string | User ID |

**Success Response (204 No Content):**
```
No body
```

**Error Responses:**
| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 | Missing/invalid token | `{"error":"UNAUTHORIZED","message":"Invalid or expired token"}` |
| 403 | Non-admin user | `{"error":"FORBIDDEN","message":"Admin access required"}` |
| 404 | User not found | `{"error":"NOT_FOUND","message":"User not found"}` |

**Frontend Usage:**
```typescript
const deleteUser = async (id: string): Promise<void> => {
  await apiClient.delete(`/api/users/${id}`);
};
```

---

### GET /api/users/{id}/orders

**Purpose:** Get all orders for a specific user
**Priority:** MEDIUM
**Auth Required:** Yes (own data) or admin (any user)
**Path Parameters:**
| Name | Type | Description |
|------|------|-------------|
| id | string | User ID |

**Query Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| page | number | 1 | Page number |
| pageSize | number | 20 | Items per page |

**Success Response (200 OK):**
```json
{
  "orders": [
    {
      "id": "ord_xxxxxxxxxxxx",
      "userId": "usr_xxxxxxxxxxxx",
      "status": "pending" | "processing" | "shipped" | "delivered" | "cancelled",
      "total": 99.99,
      "currency": "USD",
      "items": [
        {
          "productId": "prod_xxx",
          "name": "Product Name",
          "quantity": 2,
          "price": 49.99
        }
      ],
      "createdAt": "2026-06-16T00:00:00.000Z",
      "updatedAt": "2026-06-16T00:00:00.000Z"
    }
  ],
  "total": 15,
  "page": 1,
  "pageSize": 20
}
```

**Error Responses:**
| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 | Missing/invalid token | `{"error":"UNAUTHORIZED","message":"Invalid or expired token"}` |
| 403 | Accessing other user's orders (non-admin) | `{"error":"FORBIDDEN","message":"Access denied"}` |
| 404 | User not found | `{"error":"NOT_FOUND","message":"User not found"}` |

**Frontend Usage:**
```typescript
interface UserOrdersResponse {
  orders: Order[];
  total: number;
  page: number;
  pageSize: number;
}

const getUserOrders = async (userId: string, page = 1): Promise<UserOrdersResponse> => {
  return apiClient.get(`/api/users/${userId}/orders?page=${page}&pageSize=20`);
};
```

---

## Impact Assessment

### Blocked Features
| Feature | User Impact |
|---------|-------------|
| User management page | Admin cannot delete users |
| User profile page | Cannot view user's order history |

### Workaround (if any)
None available - endpoint must be implemented.

---

## Request

**Action Required:** Please implement the missing endpoints listed above.

**Suggested Implementation Order:**
1. DELETE /api/users/{id} (HIGH priority - blocking user management)
2. GET /api/users/{id}/orders (MEDIUM priority - profile enhancement)

**Backend Owner:** [Team/Person responsible for backend]
**Target Date:** [Expected implementation date]

---

*Reported: YYYY-MM-DD HH:mm*
*Frontend integration blocked until resolved*
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Assuming endpoint exists | Test with curl first, document actual response |
| Proceeding without Swagger check | Always check for OpenAPI spec first |
| Ignoring missing endpoints | Create MISSING_ENDPOINT_REPORT and request implementation |
| Implementing frontend without backend | Wait for endpoint to exist, then integrate |
| Hardcoded URL | Use environment variable `NEXT_PUBLIC_API_URL` |
| No loading state | Show spinner during API calls |
| No error handling | Show error state with retry button |
| Silent API failures | Log to error service + show user message |
| Not testing the integration | Run real E2E tests against running backend |
| Mock data in production | Use real backend with test credentials |
| Ignoring CORS errors | Configure backend CORS or use proxy |
| No type safety | Define TypeScript interfaces for all responses |

---

## Execution Checklist

```
[ ] Phase 0: Check /docs for existing API documentation
[ ] Phase 0: Verify backend is running at expected URL
[ ] Phase 0.5: Check for Swagger/OpenAPI documentation
[ ] Phase 0.5: Parse OpenAPI spec for available endpoints
[ ] Phase 0.5: Compare needed vs available endpoints
[ ] Phase 0.6: If endpoints missing, create MISSING_ENDPOINT_REPORT
[ ] Phase 0.6: Request backend implementation OR implement if authorized
[ ] Phase 1: Test each endpoint with curl (GET, POST, PATCH, DELETE)
[ ] Phase 1: Document actual request/response for each endpoint
[ ] Phase 1: Document error response formats for each endpoint
[ ] Phase 1: Create API contract TypeScript interfaces (api/contracts/*.ts)
[ ] Phase 2: Create typed API client with ApiError handling
[ ] Phase 3: Implement React hooks for data fetching
[ ] Phase 3: Add loading, error, and empty states to components
[ ] Phase 4: Run integration tests against real backend
[ ] Phase 4: Run Playwright E2E tests
[ ] Verify: Swagger/OpenAPI discovered and parsed (if available)
[ ] Verify: All needed endpoints exist (or REPORTED if missing)
[ ] Verify: All endpoints return expected status codes (curl tests)
[ ] Verify: Error responses handled gracefully (401, 403, 400, 500)
[ ] Verify: Loading states display correctly during API calls
[ ] Verify: API URL from environment variable (NEXT_PUBLIC_API_URL)
[ ] Verify: TypeScript interfaces created for all responses
[ ] Verify: Documentation complete:
[ ]   - integration-report.md with curl test results
[ ]   - MISSING_ENDPOINT_REPORT.md (if any endpoints missing)
[ ]   - api/contracts/*.ts with verified interfaces
[ ]   - FRONTEND_ARCH.md with architecture documentation
[ ]   - .env.example with required variables
```

---

## Verification

After frontend integration:
1. ✅ Backend verified running at expected URL
2. ✅ Swagger/OpenAPI discovered and parsed (if available)
3. ✅ Endpoint availability compared - all needed endpoints exist OR reported as missing
4. ✅ MISSING_ENDPOINT_REPORT created if endpoints don't exist
5. ✅ All endpoints tested with curl - actual responses documented
6. ✅ API contract interfaces created (`api/contracts/*.ts`)
7. ✅ API client has proper error handling (`ApiError` class)
8. ✅ React hooks handle loading, error, and empty states
9. ✅ Integration tests run against real backend
10. ✅ Playwright E2E tests pass
11. ✅ API URL from environment variable (`NEXT_PUBLIC_API_URL`)
12. ✅ All error cases handled (401, 403, 400, 409, 500, network)
13. ✅ Loading states display during API calls
14. ✅ **integration-report.md** created with curl test results
15. ✅ **MISSING_ENDPOINT_REPORT.md** created if backend endpoints needed
16. ✅ **FRONTEND_ARCH.md** documents project structure and architecture
17. ✅ **.env.example** contains all required environment variables
