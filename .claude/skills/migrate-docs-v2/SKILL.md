---
name: migrate-docs-v2
description: >
  Migrate a consumer repository's AsciiDoc include paths from
  gesinn-it-docs-master-pub v1 (flat snippet names) to v2 (scoped
  subdirectory structure). Use when updating the submodule pointer to v2
  causes broken include:: paths in the consumer repository's source files.
  Searches all *.adoc source files for old include paths, replaces them with
  v2 equivalents, sets up skills, and validates that no old paths remain.
  Idempotent: safe to run on a repo that is already fully migrated.
compatibility: >
  Requires gesinn-it-docs-master-pub submodule updated to v2.
  Consumer repo must have source .adoc files (not only generated output).
---

## Context

The submodule at `docs/gesinn-it-docs-master-pub` has been updated to v2,
which reorganises snippets from flat names into scoped subdirectories and
introduces pre-built skills.

**Old pattern:** `snippets/{scope}/coding-conventions-{lang}.adoc`
**New pattern:** `snippets/{scope}/conventions/{lang}.adoc`

Load `references/01-path-mapping.md` before making any changes — it contains
the complete old-to-new substitution table.

---

## Step 0: Idempotency check

Before making any changes, run the checks from `references/00-idempotency.md`
to determine which steps still need to be done.

- If **all** checks pass → report "already at v2, nothing to do" and stop.
- If **some** checks pass → skip the completed steps, continue with the rest.
- If **none** pass → proceed from Step 1.

---

## Step 1: Update submodule pointer

Check whether the submodule is already at v2:

```bash
ls docs/gesinn-it-docs-master-pub/snippets/mediawiki/conventions/ 2>/dev/null
```

If the directory exists, the submodule is already at v2 — skip this step.

Otherwise update from the local checkout of gesinn-it-docs-master-pub:

```bash
cd docs/gesinn-it-docs-master-pub
git fetch /path/to/local/gesinn-it-docs-master-pub
git checkout <HEAD-SHA>
cd ../..
```

Or update from the remote:

```bash
git submodule update --remote docs/gesinn-it-docs-master-pub
```

---

## Step 2: Locate all affected source files

Search for .adoc files that contain v1 include paths:

```bash
grep -rl "gesinn-it-docs-master-pub/snippets" . --include="*.adoc" 2>/dev/null
grep -rl "{project_type}/" . --include="*.adoc" 2>/dev/null
```

**Do not modify generated files** — skip `README.adoc`, `AGENTS.md`, and any
file under `docs/gesinn-it-docs-master-pub/`.

---

## Step 3: Apply path substitutions

Read `references/01-path-mapping.md` for the complete substitution table.
Use `references/02-regex-patterns.md` for the sed patterns.

For each source file identified in Step 2:

1. Read the full file content
2. Apply each substitution from the path mapping table
3. Show the diff before writing
4. Write the updated file

Pay special attention to files that used the `{project_type}` variable — these
must be expanded to explicit paths (e.g. `mediawiki/conventions/general.adoc`).

---

## Step 4: Slim AGENTS-source.adoc

After path migration, `AGENTS-source.adoc` may still include shared boilerplate
snippets (coding procedures, conventions, test-workflow snippets) that now
duplicate what the skills provide. Remove them following `references/04-agents-slim.md`.

**Why:** a large AGENTS.md wastes context on every agent call. Project-specific
rules belong in AGENTS.md; reusable conventions belong in skills.

---

## Step 5: Set up skills

Copy the pre-built skills from the submodule into the consumer repo's
`.claude/skills/` directory following `references/05-skills-setup.md`.

Also update `build-docs.yml` to keep skills in sync whenever the submodule changes.

---

## Step 6: Validate

Run the validation checks from `references/06-validation.md` to confirm that:

1. No old-format paths remain in any source file.
2. Shared boilerplate has been removed from `AGENTS-source.adoc`.
3. Skills are present in `.claude/skills/`.

Expected result: zero matches for all grep patterns listed in the validation
reference. If any matches remain, return to Step 3 or Step 4 and apply the
missing changes.

---

## Step 7: Commit

Use the commit template from `references/07-commit-procedure.md`.

Stage only source files and generated skill files (not README.adoc or AGENTS.md).
