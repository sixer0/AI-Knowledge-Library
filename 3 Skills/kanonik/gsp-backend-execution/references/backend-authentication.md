# Backend Authentication

## JWT Implementation

### Token Structure
```typescript
interface JWTPayload {
  sub: string;        // User ID
  email: string;
  role: string;
  iat: number;        // Issued at
  exp: number;        // Expiration
}

// Access token: short-lived (15 minutes)
// Refresh token: long-lived (7 days)
```

### Token Generation
```typescript
import jwt from 'jsonwebtoken';
import { RS256 } from './algorithms';

export function generateAccessToken(user: User): string {
  return jwt.sign(
    {
      sub: user.id,
      email: user.email,
      role: user.role,
    },
    privateKey,
    {
      algorithm: 'RS256',
      expiresIn: '15m',
      issuer: 'my-app',
      audience: 'my-app-api',
    }
  );
}

export function generateRefreshToken(user: User): string {
  return jwt.sign(
    {
      sub: user.id,
      type: 'refresh',
      jti: randomUUID(),  // Unique token ID for revocation
    },
    refreshSecret,
    {
      algorithm: 'HS256',
      expiresIn: '7d',
    }
  );
}
```

### Token Verification
```typescript
import jwt from 'jsonwebtoken';

export function verifyAccessToken(token: string): JWTPayload {
  return jwt.verify(token, publicKey, {
    algorithms: ['RS256'],
    issuer: 'my-app',
    audience: 'my-app-api',
  }) as JWTPayload;
}

export function verifyRefreshToken(token: string): { sub: string; jti: string } {
  return jwt.verify(token, refreshSecret, {
    algorithms: ['HS256'],
  }) as { sub: string; jti: string };
}
```

## OAuth 2.1 + PKCE

### Authorization Code Flow with PKCE
```typescript
// 1. Generate code verifier and challenge
import { createHash, randomBytes } from 'crypto';

function generateCodeVerifier(): string {
  return randomBytes(32).toString('base64url');
}

function generateCodeChallenge(verifier: string): string {
  return createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

// 2. Authorization URL
const codeVerifier = generateCodeVerifier();
const codeChallenge = generateCodeChallenge(codeVerifier);

const authUrl = new URL('https://auth.provider.com/authorize');
authUrl.searchParams.set('client_id', CLIENT_ID);
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', 'openid profile email');
authUrl.searchParams.set('code_challenge', codeChallenge);
authUrl.searchParams.set('code_challenge_method', 'S256');
authUrl.searchParams.set('state', generateState()); // CSRF protection

// Store codeVerifier in session for later exchange
```

### Token Exchange
```typescript
// 3. Exchange code for tokens
const response = await fetch('https://auth.provider.com/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: CLIENT_ID,
    code: authorizationCode,
    redirect_uri: REDIRECT_URI,
    code_verifier: codeVerifier,
  }),
});

const tokens = await response.json();
// { access_token, refresh_token, id_token, expires_in }
```

## Session Management

```typescript
import Redis from 'ioredis';
import { createCookie, createSessionStorage } from 'react';

const redis = new Redis(process.env.REDIS_URL);

const sessionStorage = createSessionStorage({
  cookie: {
    name: '__session',
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 7 * 24 * 60 * 60, // 7 days
  },
  store: {
    async get(id: string) {
      const data = await redis.get(`session:${id}`);
      return data ? JSON.parse(data) : null;
    },
    async set(id: string, data: any) {
      await redis.setex(`session:${id}`, 7 * 24 * 60 * 60, JSON.stringify(data));
    },
    async delete(id: string) {
      await redis.del(`session:${id}`);
    },
  },
});
```

## RBAC (Role-Based Access Control)

```typescript
// Define permissions
const Permissions = {
  USER_READ: 'user:read',
  USER_WRITE: 'user:write',
  USER_DELETE: 'user:delete',
  ORDER_READ: 'order:read',
  ADMIN_ALL: 'admin:*',
} as const;

// Role-to-permission mapping
const RolePermissions: Record<Role, Permission[]> = {
  user: [Permissions.USER_READ],
  moderator: [Permissions.USER_READ, Permissions.USER_WRITE, Permissions.ORDER_READ],
  admin: [Permissions.ADMIN_ALL],
};

// Check permission
export function hasPermission(role: Role, permission: Permission): boolean {
  const permissions = RolePermissions[role] || [];
  return permissions.includes(permission) || permissions.includes(Permissions.ADMIN_ALL);
}

// Middleware
export function requirePermission(...permissions: Permission[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    for (const permission of permissions) {
      if (!hasPermission(req.user.role, permission)) {
        return res.status(403).json({
          error: 'FORBIDDEN',
          message: `Permission denied: ${permission}`,
        });
      }
    }
    next();
  };
}

// Usage
router.delete('/users/:id', authenticate, requirePermission(Permissions.USER_DELETE), deleteUser);
```

## MFA (Multi-Factor Authentication)

```typescript
import speakeasy from 'speakeasy';

// Generate secret for user
export function generateMFASecret(): { secret: string; otpauthUrl: string } {
  return speakeasy.generateSecret({
    name: 'MyApp (user@email.com)',
    length: 20,
  });
}

// Verify TOTP
export function verifyMFA(token: string, secret: string): boolean {
  return speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 1, // Allow 1 step tolerance
  });
}

// Backup codes (store hashed)
export function generateBackupCodes(count: number = 10): string[] {
  return Array.from({ length: count }, () =>
    randomBytes(4).toString('hex').toUpperCase()
  );
}
```

## Password Reset Flow

```typescript
// 1. Request reset
export async function requestPasswordReset(email: string) {
  const user = await db.user.findUnique({ where: { email } });
  if (!user) return; // Don't reveal if user exists

  const resetToken = randomBytes(32).toString('base64url');
  const resetTokenHash = await hash(resetToken, 10);

  await db.user.update({
    where: { email },
    data: {
      resetTokenHash,
      resetTokenExpiresAt: new Date(Date.now() + 3600000), // 1 hour
    },
  });

  // Send email with resetToken (never store/email the hash)
  await sendEmail({
    to: email,
    subject: 'Password Reset',
    body: `Reset link: ${FRONTEND_URL}/reset-password?token=${resetToken}`,
  });
}

// 2. Reset password
export async function resetPassword(token: string, newPassword: string) {
  const user = await db.user.findFirst({
    where: {
      resetTokenExpiresAt: { gt: new Date() },
    },
  });

  if (!user || !await verify(user.resetTokenHash, token)) {
    throw new BadRequestError('Invalid or expired reset token');
  }

  await db.user.update({
    where: { id: user.id },
    data: {
      passwordHash: await hash(newPassword),
      resetTokenHash: null,
      resetTokenExpiresAt: null,
    },
  });
}
```

## Token Rotation Strategy

```typescript
// Refresh token rotation with reuse detection
export async function refreshAccessToken(refreshToken: string) {
  // Verify refresh token
  const payload = verifyRefreshToken(refreshToken);

  // Check if token was already used (replay attack)
  const isUsed = await redis.get(`used_refresh:${payload.jti}`);
  if (isUsed) {
    // Token reuse detected - revoke all tokens for this user
    await revokeAllUserTokens(payload.sub);
    throw new UnauthorizedError('Token reuse detected');
  }

  // Mark token as used
  await redis.setex(`used_refresh:${payload.jti}`, 30 * 24 * 60 * 60, '1');

  // Generate new tokens
  const user = await getUser(payload.sub);
  return {
    accessToken: generateAccessToken(user),
    refreshToken: generateRefreshToken(user), // New refresh token
  };
}
```