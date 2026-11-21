---
record_type: knowledge_card
reference_id: SDLC-G5
title: "Secure code review checklist, with dependency and secret checks"
domain: SDLC
phase: security
language: en
authority_status: ACTIVE
author: PT GSP
written_for: Swarm Coder
source: "Categories of the OWASP Top 10 2021 (https://owasp.org/Top10/), reworded; PT GSP security review guidance; the command table is new writing by PT GSP."
---
> SDLC library reference entry. A checklist to review against, not an instruction.
> The active harness and the current user win on any conflict.

# G5 Secure code review checklist

Written by PT GSP for Swarm Coder.
Source: Categories of the OWASP Top 10 2021 (https://owasp.org/Top10/), reworded; PT GSP security review guidance; the command table is new writing by PT GSP.

A checklist a reviewer can tick against a diff or a module. It is grouped by the categories of the OWASP Top 10 (see https://owasp.org/Top10/ for the official descriptions); the wording below is this library's own. Each line names the code smell to look for. Mark every line `ok`, `finding` or `n/a`, and record findings in the table at the end.

## 1. Broken access control

- An endpoint, handler or command acts on an object id taken from the request without checking that the caller may access that object.
- Authorisation is checked in the UI or client only, not on the server.
- Role or tenant checks are copied into each handler instead of enforced in one place; one handler forgot it.
- Directory traversal: a path built from user input without normalising it and confirming it stays under the intended root.
- CORS allows any origin together with credentials.

## 2. Cryptographic failures

- Sensitive data (passwords, tokens, personal data) stored or sent without encryption, or over plain HTTP.
- Passwords hashed with a fast hash (MD5, SHA-1, plain SHA-256) instead of a password hash (Argon2id, scrypt, bcrypt).
- Home-made cryptography, a fixed IV or nonce, ECB mode, or a key in the source.
- Random values for tokens taken from a non-cryptographic generator.
- TLS certificate verification turned off "for now".

## 3. Injection

- SQL, shell, LDAP or template strings built by concatenating input; the fix is parameters or an API that takes arguments separately.
- A shell is invoked with a single command string containing input, instead of an argument array without a shell.
- Input reaches `eval`, dynamic `import`, deserialisation of untrusted data, or a regex built from input (ReDoS).
- HTML output that does not escape by default, or that uses a raw-HTML escape hatch with user content (cross-site scripting).

## 4. Insecure design

- No limit on an expensive or abusable action (login, password reset, file upload, search, sending messages).
- A business rule (price, quantity, balance) trusted from the client.
- A multi-step flow where a later step does not check that the earlier step really happened.

## 5. Security misconfiguration

- Debug mode, stack traces or verbose errors shown to users in production.
- Default credentials, sample accounts or admin consoles left enabled.
- Missing security headers on web responses (Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options).
- Cloud storage, a database or an internal port open to the internet.
- Overly broad permissions for a service account, container or token.

## 6. Vulnerable and outdated components

- A new dependency added without checking its maintenance, licence and known advisories.
- Lockfile missing or not committed, so builds resolve different versions.
- A pinned version with a published advisory (see the command table in section 11).

## 7. Identification and authentication failures

- Session ids or tokens in URLs, logs or local storage readable by scripts.
- No expiry or revocation for sessions and tokens; logout does not invalidate server-side state.
- Account enumeration through different messages or timings for "unknown user" and "wrong password".
- Missing brute-force protection on login and one-time codes.

## 8. Software and data integrity failures

- Updates, plugins or scripts downloaded and run without a signature or hash check.
- CI pipeline steps pulled by a moving tag instead of a pinned version or digest.
- Deserialising objects whose type the attacker controls.

## 9. Logging and monitoring failures

- Security-relevant events (login failure, permission denied, admin action) not logged.
- Logs contain secrets, tokens or personal data; log a reference id instead.
- Errors swallowed without a log entry, so an attack leaves no trace.

## 10. Server-side request forgery

- The server fetches a URL supplied by the user without an allowlist of hosts and schemes.
- Redirects are followed to internal addresses, link-local ranges or cloud metadata endpoints.

## 11. Secrets

**What counts:** API keys, passwords, private keys, signing keys, OAuth client secrets, session cookies, database connection strings with credentials, webhook URLs that carry a token.

**Where they leak:** source files and config committed to the repository; test fixtures; example `.env` files filled with real values; logs and error messages; CI output; container image layers; old commits that were "fixed" later but remain in history.

**What to do on a find:**

1. Do not paste the value anywhere, including the review comment; refer to file and line.
2. Treat it as compromised: the owner rotates or revokes it at the provider first.
3. Remove it from the code and load it from the environment or a secret manager.
4. If it reached a shared history, removing it from history is a separate, approved operation; rotation is what actually protects.
5. Add a scanner rule or pre-commit hook so the same kind of value is caught next time.

## 12. Dependency audit and secret scan commands

Run a command only when the tool is installed in the project or on the host; record "not available" otherwise rather than installing tools during a review.

| Ecosystem | Audit command | Notes |
|---|---|---|
| npm | `npm audit` | `--omit=dev` to focus on shipped code |
| pnpm | `pnpm audit` | |
| Yarn | `yarn npm audit` (Berry) / `yarn audit` (classic) | |
| Bun | `bun audit` | recent Bun versions only |
| Python | `pip-audit` | reads the active environment or `-r requirements.txt` |
| Rust | `cargo audit` | needs the `cargo-audit` crate |
| Go | `govulncheck ./...` | reports only vulnerabilities in reachable code |
| Ruby | `bundle audit check --update` | needs `bundler-audit` |
| Java / Kotlin | OWASP Dependency-Check, or the build tool's audit plugin | |
| .NET | `dotnet list package --vulnerable` | |
| Containers | `trivy image <image>` or `grype <image>` | also scans OS packages |
| Secrets | `gitleaks detect` (history) / `gitleaks protect --staged` (pre-commit) | `trufflehog git file://.` is an alternative |

## 13. Verdict

| Verdict | When |
|---|---|
| PASS | No finding, or only informational notes. |
| CAUTION | Findings of low or medium severity with a clear fix or an accepted, documented risk; nothing exploitable from outside without other conditions. |
| FAIL | Any exploitable injection, broken access control, exposed secret, disabled certificate check, critical or high advisory in a shipped dependency, or a destructive operation without a guard. The change does not proceed until fixed. |

## 14. Findings

| # | Category (section) | File:line | Finding | Severity (critical / high / medium / low) | Fix | Status |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
