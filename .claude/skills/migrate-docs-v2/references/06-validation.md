# Validation Checklist

Run these checks after applying all changes.
Expected result: zero matches for grep checks, and presence checks return OK.

## 1. No old-format include paths remain

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

Expected: no output.

## 2. AGENTS-source.adoc contains no shared snippet includes

```bash
grep -E \
  "snippets/(universal/procedures|mediawiki/conventions|php/conventions|mediawiki/execution|mediawiki/procedures)" \
  AGENTS-source.adoc 2>/dev/null
```

Expected: no output.

## 3. Skills are present

```bash
ls .claude/skills/code-fix-php-mediawiki/SKILL.md 2>/dev/null \
  && echo "OK" || echo "MISSING — run skills setup step"
```

Expected: `OK`.

## 4. build-docs.yml contains skills build step

```bash
grep "build-skills.py" .github/workflows/build-docs.yml
```

Expected: one match showing the `python3 ... build-skills.py` invocation.
