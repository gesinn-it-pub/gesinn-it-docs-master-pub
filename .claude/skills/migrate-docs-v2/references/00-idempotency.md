# Idempotency Checks

Run these checks before starting. Each check is independent — skip only the
steps whose checks pass, continue with the rest.

## Check 1: Submodule at v2

```bash
ls docs/gesinn-it-docs-master-pub/snippets/mediawiki/conventions/ 2>/dev/null \
  && echo "SUBMODULE: v2" || echo "SUBMODULE: v1 — needs update"
```

Pass: directory exists.

## Check 2: Source files already migrated (no old paths)

```bash
grep -r \
  -e "snippets/universal/coding-procedure\.adoc" \
  -e "snippets/universal/coding-conventions-" \
  -e "snippets/universal/note-" \
  -e "snippets/mediawiki/coding-conventions" \
  -e "snippets/mediawiki/test-first-approach" \
  -e "snippets/mediawiki/ci-" \
  -e "snippets/nodejs/coding-conventions" \
  -e "snippets/nodejs/ci-" \
  -e "snippets/ansible/coding-conventions" \
  -e "{project_type}/" \
  . --include="*.adoc" -l 2>/dev/null \
  | grep -v "docs/gesinn-it-docs-master-pub/"
```

Pass: zero output lines.

## Check 3: AGENTS-source.adoc is lean (no shared boilerplate includes)

```bash
grep -E \
  "snippets/(universal/procedures|mediawiki/conventions|php/conventions|mediawiki/execution|mediawiki/procedures)" \
  AGENTS-source.adoc 2>/dev/null
```

Pass: zero output lines (shared snippets are in skills, not in AGENTS-source).

## Check 4: Skills are set up in this repo

```bash
ls .claude/skills/code-fix-php-mediawiki/SKILL.md 2>/dev/null \
  && echo "SKILLS: present" || echo "SKILLS: missing — needs setup"
```

Pass: file exists.

## Summary

All four checks pass → already fully migrated, nothing to do.
Any check fails → proceed with the corresponding step(s).
