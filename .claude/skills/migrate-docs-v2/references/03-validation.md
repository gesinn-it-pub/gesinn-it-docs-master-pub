# Validation Checklist

Run these grep commands after applying all substitutions.
Each command must return **zero matches** for the migration to be complete.

## Universal

```bash
# Old procedure file
grep -r "snippets/universal/coding-procedure\.adoc" . --include="*.adoc" -l

# Old conventions files
grep -r "snippets/universal/coding-conventions-" . --include="*.adoc" -l

# Old note files
grep -r "snippets/universal/note-" . --include="*.adoc" -l
```

## MediaWiki

```bash
# Old aggregator
grep -r "snippets/mediawiki/coding-conventions\.adoc" . --include="*.adoc" -l

# Old flat convention files
grep -r "snippets/mediawiki/coding-conventions-" . --include="*.adoc" -l

# Old test procedure
grep -r "snippets/mediawiki/test-first-approach" . --include="*.adoc" -l

# Old ci- files
grep -r "snippets/mediawiki/ci-" . --include="*.adoc" -l
```

## Node.js

```bash
# Old aggregator
grep -r "snippets/nodejs/coding-conventions\.adoc" . --include="*.adoc" -l

# Old flat convention files
grep -r "snippets/nodejs/coding-conventions-" . --include="*.adoc" -l

# Old ci- files
grep -r "snippets/nodejs/ci-" . --include="*.adoc" -l
```

## Ansible

```bash
# Old aggregator
grep -r "snippets/ansible/coding-conventions\.adoc" . --include="*.adoc" -l

# Old flat convention files
grep -r "snippets/ansible/coding-conventions-" . --include="*.adoc" -l
```

## Combined one-liner

Run all checks at once. Expected output: no lines printed.

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
  . --include="*.adoc" -l
```
