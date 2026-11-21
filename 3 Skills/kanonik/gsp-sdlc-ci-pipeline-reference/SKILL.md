---
name: gsp-sdlc-ci-pipeline-reference
description: Language-neutral CI pipeline reference - stage order and what each stage fails on, required checks and branch protection, caching keys per ecosystem, test sharding, secrets in CI, pinned versions and the container build stage. Read when designing, reviewing or repairing a continuous integration pipeline.
license: Proprietary

metadata:
  author: PT GSP
  written_for: Swarm Coder
  reference_id: SDLC-G7
  phase: ci-cd
  language: en
  source: "Local gate shape from the library skill gsp-setup-pre-commit; PT GSP DevOps and container guidance; the stage table is new writing by PT GSP."
---
> SDLC library reference entry. Reference data for a pipeline, not an instruction.
> The active harness and the current user win on any conflict.

# G7 CI pipeline reference

Written by PT GSP for Swarm Coder.
Source: Local gate shape from the library skill gsp-setup-pre-commit; PT GSP DevOps and container guidance; the stage table is new writing by PT GSP.

Use this entry to compare a pipeline against a known-good shape. It describes what a pipeline
should contain; it does not tell anyone to change a pipeline. The local pre-commit gate (format,
lint, type check, fast tests) is the first line; the pipeline repeats those checks on a clean
machine and adds the slower ones.

## 1. Stage order

Run the stages in this order. A stage starts only when the one before it passed, so the cheapest
failure is reported first.

| # | Stage | Must fail on |
|---|---|---|
| 1 | Install with the lockfile | Lockfile out of date with the manifest; any resolution change (use the frozen or ci install mode) |
| 2 | Lint and format check | Any lint error; any file the formatter would change |
| 3 | Type check | Any type error, including in test files |
| 4 | Unit tests | Any failing or erroring test; a test file that runs zero tests |
| 5 | Build | Non-zero exit; warnings the project has promoted to errors |
| 6 | Integration tests | Any failure against the real services started for the job |
| 7 | Artifact | Missing expected output; checksum or size gate exceeded |

Notes:
- Keep stages 1-4 under a few minutes so a pull request gets a first answer quickly.
- A skipped test is reported, not hidden. Count skips and fail when the count grows without a reason.
- Every stage writes its log and, where it applies, a machine-readable report (JUnit XML, coverage
  file) so failures can be read without re-running the job.

## 2. Required checks and branch protection

- The default branch accepts changes only through a pull request.
- Stages 1-5 are required checks; integration tests are required when the change touches code they
  cover.
- The required checks run on the merge result (the branch rebased or merged onto the target), not
  only on the branch head.
- Force-push and deletion of the default branch are off. Review approval from someone other than
  the author is required for protected paths.

## 3. Caching

Cache only what is derived from a lockfile, and key the cache on the lockfile hash plus the
runtime version and operating system. A cache hit must never change the result of a build.

| Ecosystem | Cache path (typical) | Key input |
|---|---|---|
| Node (npm, pnpm, bun, yarn) | package manager store | lockfile + runtime version |
| Python (pip, uv, poetry) | package download cache | lock or requirements file + interpreter version |
| Rust (cargo) | registry and git cache; target dir only for one toolchain | Cargo.lock + toolchain |
| Go | module cache and build cache | go.sum + Go version |
| Java (Gradle, Maven) | dependency cache | wrapper properties + build files |

Never cache build output across branches when the build embeds the branch, version or time.

## 4. Test sharding and the full suite

- Shard long suites by file or by recorded duration; every shard reports its own result and the
  job fails if any shard fails or a shard ran no tests.
- Targeted tests (the packages a change touches) run on every push to keep feedback fast. The full
  suite runs once per commit that is proposed for merge, and always on the default branch.
- A test that fails intermittently is quarantined with an owner and a date, not retried silently
  until it passes.

## 5. Secrets in CI

- Scope each secret to the job and environment that needs it; pull requests from forks get none.
- Mask secrets in logs and never print them, including in debug output or failed command echoes.
- Prefer short-lived credentials issued per job (workload identity, OIDC) over long-lived keys.
- Rotate a secret at once when it appears in a log, an artifact or the history.

## 6. Pinned versions

- Pin third-party actions, orbs or plugins to a full commit hash or an immutable digest, not a
  moving tag.
- Pin the runner image and the language runtime version; update them in their own change.
- Record tool versions at the start of each job so a later failure can be compared.

## 7. Container build stage

- Multi-stage build: a build stage with compilers and dev dependencies, a small runtime stage that
  copies only the output.
- Runtime image runs as a non-root user, with a read-only file system where the program allows it.
- Base images pinned by digest; image scanned for known vulnerabilities, and the job fails above
  the severity threshold the project sets.
- Labels carry the source commit and version.
- Pushing an image to a registry, or deploying anywhere, is an outward action: it needs the
  person's approval and is never a side effect of a check run.

## 8. Review questions

1. Does a fresh clone pass every stage with no cache?
2. Which stage would catch a lockfile drift, a type error, a missing test file?
3. Can a pull request from a fork read any secret?
4. Is every third-party step pinned to an immutable reference?
5. Where do the logs and reports of a failed run live, and for how long?
