# Sed Substitution Patterns

Use these patterns for mechanical path substitutions. Apply with:
`sed -i 's|OLD|NEW|g' filename.adoc`

Or use the Read/Edit tools to apply substitutions interactively.

## Universal

```bash
# note-generated-file.adoc
sed -i 's|snippets/universal/note-generated-file\.adoc|snippets/universal/notes/generated-file.adoc|g'

# note-contains-submodule.adoc
sed -i 's|snippets/universal/note-contains-submodule\.adoc|snippets/universal/notes/contains-submodule.adoc|g'

# coding-conventions-general.adoc (universal)
sed -i 's|snippets/universal/coding-conventions-general\.adoc|snippets/universal/conventions/general.adoc|g'

# coding-conventions-docker.adoc
sed -i 's|snippets/universal/coding-conventions-docker\.adoc|snippets/universal/conventions/docker.adoc|g'
```

**`coding-procedure.adoc` requires manual replacement** (one include → four includes).
Search for: `snippets/universal/coding-procedure.adoc`

## MediaWiki

```bash
# coding-conventions-general.adoc (mediawiki)
sed -i 's|snippets/mediawiki/coding-conventions-general\.adoc|snippets/mediawiki/conventions/general.adoc|g'

# coding-conventions-js.adoc (mediawiki)
sed -i 's|snippets/mediawiki/coding-conventions-js\.adoc|snippets/mediawiki/conventions/js.adoc|g'

# coding-conventions-css.adoc (mediawiki)
sed -i 's|snippets/mediawiki/coding-conventions-css\.adoc|snippets/mediawiki/conventions/css.adoc|g'

# coding-conventions-phan.adoc → php/conventions/phan.adoc
sed -i 's|snippets/mediawiki/coding-conventions-phan\.adoc|snippets/php/conventions/phan.adoc|g'

# test-first-approach.adoc
sed -i 's|snippets/mediawiki/test-first-approach\.adoc|snippets/mediawiki/procedures/test-write-php-mediawiki.adoc|g'

# ci-install.adoc
sed -i 's|snippets/mediawiki/ci-install\.adoc|snippets/mediawiki/execution/install-deps.adoc|g'

# ci-phpunit.adoc
sed -i 's|snippets/mediawiki/ci-phpunit\.adoc|snippets/mediawiki/execution/run-tests-phpunit.adoc|g'

# ci-phan.adoc
sed -i 's|snippets/mediawiki/ci-phan\.adoc|snippets/mediawiki/execution/run-phan.adoc|g'

# ci-npm.adoc (mediawiki)
sed -i 's|snippets/mediawiki/ci-npm\.adoc|snippets/mediawiki/execution/run-tests-npm.adoc|g'

# ci-pre-commit.adoc
sed -i 's|snippets/mediawiki/ci-pre-commit\.adoc|snippets/mediawiki/execution/run-pre-commit.adoc|g'
```

**`coding-conventions-php.adoc` requires manual replacement** — it splits into two files:
- `snippets/php/conventions/php.adoc` (base PHP rules)
- `snippets/mediawiki/conventions/php.adoc` (MediaWiki-specific delta)

Search for: `snippets/mediawiki/coding-conventions-php.adoc`

**`coding-conventions.adoc` (aggregator) requires manual replacement** — see
`references/01-path-mapping.md` for the expanded include list.

Search for: `snippets/mediawiki/coding-conventions.adoc`

## Node.js

```bash
# coding-conventions-js.adoc (nodejs)
sed -i 's|snippets/nodejs/coding-conventions-js\.adoc|snippets/nodejs/conventions/js.adoc|g'

# ci-npm.adoc (nodejs)
sed -i 's|snippets/nodejs/ci-npm\.adoc|snippets/nodejs/execution/run-npm.adoc|g'

# ci-mocha.adoc
sed -i 's|snippets/nodejs/ci-mocha\.adoc|snippets/nodejs/execution/run-tests-mocha.adoc|g'

# ci-publish.adoc
sed -i 's|snippets/nodejs/ci-publish\.adoc|snippets/nodejs/execution/publish.adoc|g'
```

**`coding-conventions.adoc` (aggregator) requires manual replacement** — see
`references/01-path-mapping.md`.

## Ansible

```bash
# coding-conventions-ansible.adoc
sed -i 's|snippets/ansible/coding-conventions-ansible\.adoc|snippets/ansible/conventions/ansible.adoc|g'

# coding-conventions-molecule.adoc
sed -i 's|snippets/ansible/coding-conventions-molecule\.adoc|snippets/ansible/conventions/molecule.adoc|g'

# coding-conventions-yaml.adoc
sed -i 's|snippets/ansible/coding-conventions-yaml\.adoc|snippets/ansible/conventions/yaml.adoc|g'
```

**`coding-conventions.adoc` (aggregator) requires manual replacement** — see
`references/01-path-mapping.md`.
