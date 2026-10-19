---
name: gsp-security-review-gate
description: >-
  Run a structured security-focused review before destructive operations,
  external actions, or changes with security implications. Checks for
  common vulnerability patterns, credential leaks, unsafe operations, and
  data exposure risks. Provides a pass/fail assessment with actionable
  remediation guidance.
license: MIT
metadata:
  hermes:
    tags: [gsp, security]
    category: security
  category: safety
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/security-review-gate
    license_path: LICENSE
---

# Security Review Gate

Run a structured security review before executing actions that could
introduce vulnerabilities, leak credentials, expose data, or cause
harm. The gate evaluates the proposed action against a checklist of
common security risks and returns a pass/fail decision with remediation
steps.

---

## Triggers

Use this skill when:
- "security review before action"
- "check for vulnerabilities"
- "scan for security issues"
- "review destructive command"
- "security gate for external calls"
- "audit this change for risks"
- "run a security check on this operation"
- "security audit required"

Do NOT use for routine, read-only operations with no security impact
(e.g., reading a file, searching the web), or when a security review
was already performed and no relevant changes have occurred since.

---

## Process

### Phase 0: Action Classification

Classify the proposed action by its security risk profile:

```markdown
## Security Review: <action description>

**Action type:** <operation being reviewed>
**Proposed by:** <who initiated>

**Risk profile:**
| Dimension | Assessment |
|-----------|------------|
| **Data access** | <read / write / delete / transmit / execute> |
| **Data sensitivity** | <public / internal / confidential / secret> |
| **External interaction** | <none / outbound API / inbound / credential use> |
| **Destructive potential** | <none / moderate / high / irreversible> |
| **Scope** | <local / network / filesystem / cross-service> |
```

**Security review levels:**

| Level | Trigger | Effort |
|-------|---------|--------|
| **L1 — Quick Scan** | Read-only access to non-sensitive data | ~30s |
| **L2 — Standard Review** | Write/modify operations, external API calls, credential use | ~2min |
| **L3 — Deep Audit** | Destructive operations, sensitive data access, cross-service actions | ~5min |
| **L4 — Full Security Audit** | Production deployment, auth changes, encryption operations | Requires user approval for each check |

---

### Phase 1: Run Security Checks

Based on the risk profile, run applicable checks:

#### 1. Credential Leak Check

For any action involving file write, API call, or data transmission:

```markdown
### Credential Leak Check

**Scope:** <what is being inspected>
**Patterns scanned:**
- [ ] API keys / tokens (`sk-...`, `api_key=...`, `token=...`)
- [ ] Passwords / secrets (`password=...`, `secret=...`, `PASSWORD`)
- [ ] Connection strings (`connection_string=...`, `mongodb://...`)
- [ ] Private keys (`-----BEGIN ... PRIVATE KEY-----`)
- [ ] Environment variable exports with secrets (`export SECRET=`)

**Findings:** <none / pattern found at <location>>
**Result:** PASS / FAIL
```

**Rules:**
- Scan all file contents being written for credential patterns
- Scan command strings for inline secrets
- Scan API call parameters for sensitive values
- If credentials are found: FAIL with location and remediation

#### 2. Destructive Operation Check

For any action that modifies or deletes data:

```markdown
### Destructive Operation Check

**Operation:** <command or action>
**What it does:** <plain language description>

**Impact assessment:**
- [ ] Files affected: <count> — <paths>
- [ ] Irreversible: <yes/no — if yes, describe>
- [ ] Data loss risk: <none / partial / complete>
- [ ] Rollback available: <yes/no — describe>

**Dry-run available?** <yes/no — if yes, recommend dry-run first>
**Result:** PASS / FAIL / CAUTION
```

**Rules:**
- FAIL if operation is irreversible with no rollback plan
- CAUTION if operation affects >10 files or modifies critical paths
- Always note if a dry-run is available

#### 3. External Call Check

For any action that reaches an external service:

```markdown
### External Call Check

**Target:** <URL or service>
**Method:** <HTTP method / protocol>
**Data being sent:** <summary of payload>

**Risk assessment:**
- [ ] TLS/HTTPS: <yes/no>
- [ ] Authentication: <method>
- [ ] Data sensitivity matched to destination trust level: <yes/no>
- [ ] Rate limiting respected: <yes/no>
- [ ] Proper error handling for network failures: <yes/no>

**Result:** PASS / FAIL
```

**Rules:**
- FAIL if non-TLS endpoint receives sensitive data
- FAIL if destination trust level is unknown or lower than data sensitivity
- CAUTION if no error handling for network or auth failures

#### 4. Code/Command Injection Check

For any action that constructs or executes commands:

```markdown
### Injection Check

**Context:** <shell command, SQL query, eval, or dynamic execution>

**Checks:**
- [ ] Input properly escaped/sanitized: <yes/no/na>
- [ ] No string concatenation of untrusted input into commands: <yes/no/na>
- [ ] Parameterized queries used where applicable: <yes/no/na>
- [ ] Shell metacharacters handled: <yes/no/na>

**Result:** PASS / FAIL
```

**Rules:**
- FAIL if untrusted input is concatenated into shell commands or SQL
- FAIL if `eval()` or `exec()` is used with unsanitized input
- CAUTION if any string interpolation of user input into commands

#### 5. Permission Escalation Check

For any action that changes access or permissions:

```markdown
### Permission Escalation Check

**Action:** <chmod, chown, ACL change, role assignment>

**Checks:**
- [ ] Least privilege principle maintained: <yes/no>
- [ ] Change is scoped to minimum required: <yes/no>
- [ ] No unintended access granted: <yes/no>

**Result:** PASS / FAIL
```

---

### Phase 2: Assess Results

Aggregate all check results into a decision:

```markdown
## Security Review Results

| Check | Result | Details |
|-------|--------|---------|
| Credential Leak | PASS / FAIL | <summary> |
| Destructive Operation | PASS / FAIL / CAUTION | <summary> |
| External Call | PASS / FAIL / CAUTION | <summary> |
| Injection | PASS / FAIL | <summary> |
| Permission Escalation | PASS / FAIL / NA | <summary> |

**Overall:** PASS / FAIL / CAUTION

### Decision Rules

| Overall | Meaning | Action |
|---------|---------|--------|
| **PASS** | No security issues found | Safe to proceed |
| **CAUTION** | Minor risks identified (≥1 CAUTION, no FAIL) | Proceed with noted mitigations, or gate for user approval |
| **FAIL** | Critical security issues found (≥1 FAIL) | Do NOT proceed. Present remediation steps. |
```

---

### Phase 3: Remediation Guidance

If the review FAILs, provide specific remediation:

```markdown
## Remediation Required

### Issue 1: <check name> — FAIL

**Location:** <exact path or code location>
**Vulnerability:** <what is wrong>
**Risk:** <what could happen>

**Fix:**
```
<before>  →  <after>
```

**Verification:** <how to confirm the fix works>
```

**Remediation rules:**
- Each FAIL must have a corresponding remediation entry
- Remediation must be specific and actionable (not "fix the issue")
- Include before/after examples where applicable
- After remediation, re-run the specific failed check

---

### Phase 4: Approval Gate

If the review results in FAIL or CAUTION:

```markdown
## Security Gate Active

**Review level:** <L1 / L2 / L3 / L4>
**Result:** <FAIL / CAUTION>
**Findings:** <summary>

**Awaiting user decision:**
1. **Apply remediation** — Let me fix the issues and re-review
2. **Override** — Proceed despite findings (user accepts the risk)
3. **Abort** — Cancel the operation entirely
```

**Gate rules:**
- FAIL requires user decision before proceeding (never auto-override)
- CAUTION may proceed if user pre-approved caution-level risks, or gate
- L4 level always requires user approval regardless of result

---

### Phase 5: Log Security Review

Record the review for audit trail:

```markdown
## Security Review Log

| # | Timestamp | Action | Level | Result | Decision | Reviewer |
|---|-----------|--------|-------|--------|----------|----------|
| 1 | 12:00:00 | rm -rf ./temp | L2 | FAIL → PASS | Applied fix | agent |
| 2 | 12:05:00 | POST to api.example.com | L2 | CAUTION | Proceeded | user |
```

**Log rules:**
- Record every review, regardless of result
- Include the before/after if remediation was applied
- Store log in a dedicated security log file when performing multiple reviews

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Skipping credential checks on file write operations | Always check written content for credential patterns |
| Auto-overriding FAIL results | FAIL always requires user decision |
| Using regex-only credential detection (high false positive) | Use pattern matching + context validation |
| Only scanning for known patterns (misses novel vulnerabilities) | Apply principle of least privilege and common-sense checks |
| Security theater — checking everything superficially | Tailor check depth to the action's risk profile |
| Treating CAUTION the same as PASS | CAUTION means "proceed with awareness" — not "nothing to see" |
| No remediation for findings | Every FAIL must have a corresponding fix suggestion |

---

## Execution Checklist

```
[ ] Phase 0: Action classified (risk profile, review level)
[ ] Phase 1: Credential Leak Check (scan written content and commands)
[ ] Phase 1: Destructive Operation Check (impact, reversibility, rollback)
[ ] Phase 1: External Call Check (TLS, auth, data sensitivity)
[ ] Phase 1: Injection Check (shell, SQL, eval — input sanitization)
[ ] Phase 1: Permission Escalation Check (least privilege, scope)
[ ] Phase 2: Results aggregated and decision (PASS / CAUTION / FAIL)
[ ] Phase 3: Remediation provided for each FAIL
[ ] Phase 4: Approval gate applied if FAIL or CAUTION
[ ] Phase 5: Security review logged for audit trail
[ ] Verify: No FAIL results were auto-overridden
[ ] Verify: Credential check scanned all written content
[ ] Verify: Remediation is specific and actionable
[ ] Verify: Dry-run availability noted for destructive operations
```

---

## Verification

After security review:
1. All applicable checks (credential, destructive, external, injection, permission) were run
2. No sensitive data (credentials, secrets) was included in any written output or command
3. Every FAIL finding has a corresponding, actionable remediation
4. User approval was obtained for FAIL results before proceeding
5. Security review log captures the action, level, result, and decision
6. Dry-run was recommended (and ideally executed) for destructive operations
7. The review did not introduce new security issues (e.g., credential scanning didn't log secrets)
