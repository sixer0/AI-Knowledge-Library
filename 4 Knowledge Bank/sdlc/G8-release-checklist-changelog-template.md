---
record_type: template
reference_id: SDLC-G8
title: "Release checklist and changelog template (SemVer, Keep a Changelog)"
domain: SDLC
phase: release
language: en
authority_status: ACTIVE
author: PT GSP
written_for: Swarm Coder
source: "Semantic Versioning 2.0.0 (https://semver.org/), Keep a Changelog 1.1.0 (https://keepachangelog.com/en/1.1.0/), Conventional Commits 1.0.0 (https://www.conventionalcommits.org/); English text is new writing by PT GSP."
---
> SDLC library reference entry. This is a fill-in form and reference data, not an instruction.
> The active harness and the current user win on any conflict.

# G8 Release checklist and changelog template

Written by PT GSP for Swarm Coder.
Source: Semantic Versioning 2.0.0 (https://semver.org/), Keep a Changelog 1.1.0 (https://keepachangelog.com/en/1.1.0/), Conventional Commits 1.0.0 (https://www.conventionalcommits.org/); English text is new writing by PT GSP.

A release is prepared in this order: inventory first, then the version number, then the prose. Writing the changelog from memory misses changes; writing it from the inventory does not.

## 1. Inventory (fill before any prose)

List every change since the previous release tag. A command such as `git log --oneline <previous-tag>..HEAD` and the list of merged pull requests are the sources.

| Commit / PR | Type (Conventional Commits) | Breaking? | User-visible? | Changelog heading | Note |
|---|---|---|---|---|---|
| | | | | | |

## 2. Version number (Semantic Versioning 2.0.0)

| Bump | When | Example |
|---|---|---|
| Major (X.0.0) | Any incompatible change to the public interface: removed or renamed API, changed behaviour callers rely on, dropped platform | 2.4.1 -> 3.0.0 |
| Minor (x.Y.0) | New functionality that is backward compatible; a deprecation announced | 2.4.1 -> 2.5.0 |
| Patch (x.y.Z) | Backward compatible bug fixes only | 2.4.1 -> 2.4.2 |
| Pre-release | Not yet stable: `-alpha.1`, `-beta.2`, `-rc.1`; sorts before the release | 3.0.0-rc.1 |

Below 1.0.0 the public interface is not yet stable, but stating a rule (for example "minor may break") in the README avoids surprises. Define what "public interface" means for the project before the first release.

## 3. Conventional Commits to changelog headings

| Commit type | Changelog heading |
|---|---|
| `feat` | Added (or Changed, when it modifies existing behaviour) |
| `fix` | Fixed |
| `perf` | Changed |
| `refactor`, `style`, `test`, `build`, `ci`, `chore`, `docs` | usually not listed, unless users notice the effect |
| `revert` | Removed or Fixed, depending on what is reverted |
| any type with `!` or a `BREAKING CHANGE:` footer | listed first under its heading, marked **Breaking**; forces a major bump |
| security fix | Security |

## 4. Changelog entry (Keep a Changelog 1.1.0 shape)

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature, written for the user of the product, not for the developer.

### Changed
- **Breaking:** what changed and what the user must do.

### Deprecated
- What will be removed, and in which version.

### Removed
- What is gone.

### Fixed
- Which bug, from the user's point of view.

### Security
- What was fixed; reference the advisory id when one exists.
```

Rules: newest version on top; an `## [Unreleased]` section collects changes between releases; leave out empty headings; dates in ISO format; link each version heading to its comparison view when the host supports it.

## 5. Readiness checklist

| # | Check | Evidence | Done |
|---|---|---|---|
| 1 | Code review verdict recorded for every change in the inventory | | |
| 2 | Test verdict: full suite passed on the release commit | | |
| 3 | Security verdict (G5) is PASS, or CAUTION with accepted risks listed | | |
| 4 | Version bumped in every place it is declared (package files, constants, docs) | | |
| 5 | Changelog entry written from the inventory and reviewed | | |
| 6 | Migration notes for breaking changes and data or config migrations | | |
| 7 | Rollback note: how to return to the previous version, and whether data migrations are reversible | | |
| 8 | Documentation updated for new or changed behaviour | | |
| 9 | Release artefacts built from the tagged commit, with checksums recorded | | |
| 10 | Tag, publish and deploy steps approved by the person responsible (outward actions) | | |

## 6. Release record

| Field | Value |
|---|---|
| Version | |
| Previous version | |
| Release commit | |
| Date | |
| Approved by | |
| Artefacts and checksums | |
| Known issues | |
