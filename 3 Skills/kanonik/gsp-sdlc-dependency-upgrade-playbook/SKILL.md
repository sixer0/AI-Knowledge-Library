---
name: gsp-sdlc-dependency-upgrade-playbook
description: Dependency upgrade and deprecation playbook - inventory outdated packages per ecosystem, read changelogs first, one upgrade per change set, lockfile as a single-writer resource, expand and contract for removing an old API, rollback and changelog notes. Read when planning or reviewing a dependency upgrade or the removal of a deprecated API.
license: Proprietary

metadata:
  author: PT GSP
  written_for: Swarm Coder
  reference_id: SDLC-G10
  phase: maintenance
  language: en
  source: "Expand and contract pattern as described in the library skill gsp-to-issues; single-writer lockfile rule from PT GSP orchestration practice; the command table is new writing by PT GSP."
---
> SDLC library reference entry. Reference data for upgrades, not an instruction.
> The active harness and the current user win on any conflict.

# G10 Dependency upgrade and deprecation playbook

Written by PT GSP for Swarm Coder.
Source: Expand and contract pattern as described in the library skill gsp-to-issues; single-writer lockfile rule from PT GSP orchestration practice; the command table is new writing by PT GSP.

## 1. Inventory

List what is outdated before changing anything. These commands only read; run them only when the
tool is installed.

| Ecosystem | Outdated list | Why-is-it-here |
|---|---|---|
| npm / pnpm / yarn / bun | `npm outdated`, `pnpm outdated`, `yarn outdated`, `bun outdated` | `npm explain <pkg>`, `pnpm why <pkg>` |
| Python | `pip list --outdated`, `uv pip list --outdated` | `pipdeptree -r -p <pkg>` |
| Rust | `cargo outdated` | `cargo tree -i <pkg>` |
| Go | `go list -u -m all` | `go mod why <module>` |
| Ruby | `bundle outdated` | `bundle exec gem dependency <gem> -R` |

For each candidate record: current version, target version, kind of bump (major, minor, patch),
and whether the package is direct or transitive.

## 2. Read before you bump

- Read the changelog or release notes between the current and the target version; list every
  breaking change, removal and deprecation.
- Check the supported runtime range of the target version against the project's runtime.
- A security advisory raises the priority, not the size of the change set.

## 3. One upgrade per change set

- Upgrade one package (or one tightly coupled family, such as a framework and its plugins) per
  change set, so a failure points at one cause and a revert undoes one thing.
- The lockfile is a single-writer resource: one change at a time writes it, and two parallel
  upgrades never both regenerate it.
- Commit the manifest and the lockfile together; never hand-edit a lockfile.
- Run the targeted tests of the packages that use the dependency first, then the full suite once
  for the change set.

## 4. Expand and contract for removing an old API

Use this shape when an API (own or third-party) is deprecated and call sites must move.

1. Expand: add the new form next to the old one; both work.
2. Migrate: move call sites in batches. Size each batch by its blast radius, found with a
   reference or call-graph search; keep each batch reviewable and green.
3. Guard: mark the old form deprecated and add a check that fails on new uses of it.
4. Contract: when no call site is left, delete the old form in its own change set.

Never combine the expand step and the contract step in one change.

## 5. Rollback

- Write the rollback before merging: usually revert the change set, restoring the previous
  manifest and lockfile.
- Note anything a revert does not undo: data migrations, changed file formats, cached artifacts,
  published packages.

## 6. What to record

| Field | Content |
|---|---|
| Package | name, from version, to version, bump kind |
| Reason | security fix, feature needed, end of support, routine |
| Breaking changes | list from the changelog, and how each was handled |
| Tests | targeted suites run, full suite result |
| Rollback | revert reference and anything a revert does not undo |
| Changelog | entry under Changed, or Security for an advisory fix; Removed for a deleted API |

## 7. Review questions

1. Is this change set one upgrade, and does the lockfile change only for it?
2. Were the breaking changes between the two versions read and listed?
3. For a removal, is every call site migrated before the old form is deleted?
4. Can the change be reverted cleanly, and what would a revert leave behind?
