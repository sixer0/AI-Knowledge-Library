# Backend Security Best Practices

## OWASP Top 10 (2025)

### A01 - Broken Access Control
```typescript
// ❌ NEVER trust client-side checks
const isAdmin = req.body.isAdmin; // From client!

// ✅ Always verify on server
const user = await getUser(req.user.id);
if (user.role !== 'admin') {
  throw new ForbiddenError('Admin access required');
}
```

### A02 - Cryptographic Failures
```typescript
// ❌ Never store plain text passwords
await db.user.create({ data: { password: req.body.password } });

// ✅ Use Argon2id (best) or bcrypt
import argon2 from 'argon2';
const hashedPassword = await argon2.hash(req.body.password, {
  type: argon2.argon2id,
  memoryCost: 65536,    // 64 MB
  timeCost: 3,          // 3 iterations
  parallelism: 4,
});

// Verify
const isValid = await argon2.verify(hashedPassword, inputPassword);
```

### A03 - Injection
```typescript
// ❌ SQL Injection possible
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅ Parameterized queries
const user = await prisma.user.findUnique({
  where: { email }, // Prisma automatically escapes
});

// ✅ Raw SQL with parameters
const result = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);
```

### A04 - Insecure Design
```typescript
// ✅ Rate limiting per user/IP
import rateLimit from 'express-rate-limit';
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => req.ip,
});

// ✅ Input validation with Zod
import { z } from 'zod';
const UserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(8).max(128),
});
```

### A05 - Security Misconfiguration
```typescript
// ✅ Security headers
import helmet from 'helmet';
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));

// ✅ CORS configuration
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true,
}));
```

### A06 - Vulnerable Components
```bash
# Regularly audit dependencies
npm audit
npx known-security-vulnerabilities

# Update regularly
npm update
```

### A07 - Auth Failures
```typescript
// ✅ JWT with RS256 (asymmetric)
const token = jwt.sign(payload, privateKey, {
  algorithm: 'RS256',
  expiresIn: '15m',
});

const payload = jwt.verify(token, publicKey);

// ✅ Refresh token rotation
await refreshToken.rotate();
```

### A08 - Data Integrity Failures
```typescript
// ✅ Sign sensitive data
import { createHmac } from 'crypto';
const signature = createHmac('sha256', secret)
  .update(data)
  .digest('hex');

// Verify before processing
const isValid = timingSafeEqual(
  Buffer.from(signature),
  Buffer.from(providedSignature)
);
```

### A09 - Logging & Monitoring
```typescript
// ✅ Structured logging with correlation ID
logger.info({
  correlationId: req.correlationId,
  event: 'user.login',
  userId: user.id,
  ip: req.ip,
  userAgent: req.headers['user-agent'],
});
```

### A10 - SSRF Protection
```typescript
// ❌ Never fetch user-provided URLs directly
const response = await fetch(userInputUrl);

// ✅ Validate URLs against allowlist
const allowedHosts = ['api.myapp.com', 'cdn.myapp.com'];
const url = new URL(userInputUrl);
if (!allowedHosts.includes(url.hostname)) {
  throw new BadRequestError('URL not allowed');
}
```

## Input Validation

```typescript
import { z } from 'zod';

// String validation
z.string().min(1).max(255);
z.string().email();
z.string().url();
z.string().uuid();
z.string().regex(/^[a-zA-Z0-9]+$/);

// Number validation
z.number().min(0).max(1000);
z.number().int();
z.number().positive();

// Complex schemas
const CreateOrderSchema = z.object({
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().min(1).max(99),
  })).min(1).max(50),
  shippingAddress: AddressSchema,
  promoCode: z.string().optional(),
});

// Custom validation
z.string().refine(
  (val) => !val.includes('<script>'),
  'Invalid characters detected'
);
```

## Security Headers Checklist

```typescript
// helmet() sets most headers automatically
app.use(helmet());

// Manual headers
res.setHeader('X-Content-Type-Options', 'nosniff');
res.setHeader('X-Frame-Options', 'DENY');
res.setHeader('X-XSS-Protection', '1; mode=block');
res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
res.setHeader('Permissions-Policy', 'geolocation=(), microphone=()');
```

## Secrets Management

```typescript
// ❌ Never hardcode secrets
const JWT_SECRET = 'my-secret-key';

// ✅ Use environment variables with validation
import 'dotenv/config';
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default('15m'),
  NODE_ENV: z.enum(['development', 'production']).default('development'),
});

const env = envSchema.parse(process.env);

// ✅ For production, use secret managers
// AWS Secrets Manager, HashiCorp Vault, etc.
```

## Encryption

```typescript
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

// AES-256-GCM for data at rest
const algorithm = 'aes-256-gcm';
const key = Buffer.from(process.env.ENCRYPTION_KEY!, 'hex');

function encrypt(text: string): string {
  const iv = randomBytes(16);
  const cipher = createCipheriv(algorithm, key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}

function decrypt(data: string): string {
  const [ivHex, authTagHex, encrypted] = data.split(':');
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');
  const decipher = createDecipheriv(algorithm, key, iv);
  decipher.setAuthTag(authTag);
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}
```