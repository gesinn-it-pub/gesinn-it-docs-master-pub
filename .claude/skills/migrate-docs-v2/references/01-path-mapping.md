# v1 → v2 Path Mapping

Complete substitution table for migrating include paths from v1 (flat) to v2 (scoped).

The consumer-repo prefix `docs/gesinn-it-docs-master-pub/` is shown in the table.
For files inside the submodule itself, use the path without the prefix.

## Universal snippets

| v1 path (consumer form) | v2 path |
|---|---|
| `docs/gesinn-it-docs-master-pub/snippets/universal/coding-conventions-general.adoc` | `docs/gesinn-it-docs-master-pub/snippets/universal/conventions/general.adoc` |
| `docs/gesinn-it-docs-master-pub/snippets/universal/coding-conventions-docker.adoc` | `docs/gesinn-it-docs-master-pub/snippets/universal/conventions/docker.adoc` |
| `docs/gesinn-it-docs-master-pub/snippets/universal/coding-procedure.adoc` | _(split — see below)_ |
| `docs/gesinn-it-docs-master-pub/snippets/universal/note-generated-file.adoc` | `docs/gesinn-it-docs-master-pub/snippets/universal/notes/generated-file.adoc` |
| `docs/gesinn-it-docs-master-pub/snippets/universal/note-contains-submodule.adoc` | `docs/gesinn-it-docs-master-pub/snippets/universal/notes/contains-submodule.adoc` |

**`coding-procedure.adoc` was split into four files.** Replace a single include of
`coding-procedure.adoc` with four separate includes:

```adoc
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/code-write.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/code-fix.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/code-refactor.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/test-write.adoc[]
```

## MediaWiki snippets

| v1 path | v2 path |
|---|---|
| `snippets/mediawiki/coding-conventions.adoc` | _(aggregator removed — include conventions individually)_ |
| `snippets/mediawiki/coding-conventions-general.adoc` | `snippets/mediawiki/conventions/general.adoc` |
| `snippets/mediawiki/coding-conventions-php.adoc` | `snippets/php/conventions/php.adoc` + `snippets/mediawiki/conventions/php.adoc` |
| `snippets/mediawiki/coding-conventions-phan.adoc` | `snippets/php/conventions/phan.adoc` |
| `snippets/mediawiki/coding-conventions-js.adoc` | `snippets/mediawiki/conventions/js.adoc` |
| `snippets/mediawiki/coding-conventions-css.adoc` | `snippets/mediawiki/conventions/css.adoc` |
| `snippets/mediawiki/test-first-approach.adoc` | `snippets/mediawiki/procedures/test-write-php-mediawiki.adoc` |
| `snippets/mediawiki/ci-install.adoc` | `snippets/mediawiki/execution/install-deps.adoc` |
| `snippets/mediawiki/ci-phpunit.adoc` | `snippets/mediawiki/execution/run-tests-phpunit.adoc` |
| `snippets/mediawiki/ci-phan.adoc` | `snippets/mediawiki/execution/run-phan.adoc` |
| `snippets/mediawiki/ci-npm.adoc` | `snippets/mediawiki/execution/run-tests-npm.adoc` |
| `snippets/mediawiki/ci-pre-commit.adoc` | `snippets/mediawiki/execution/run-pre-commit.adoc` |

**`coding-conventions.adoc` (aggregator) was removed.** Replace a single include of
`coding-conventions.adoc` with explicit includes for each convention file needed:

```adoc
include::snippets/mediawiki/conventions/general.adoc[]
include::snippets/universal/conventions/general.adoc[]
include::snippets/php/conventions/php.adoc[]
include::snippets/mediawiki/conventions/php.adoc[]
include::snippets/php/conventions/phan.adoc[]
include::snippets/mediawiki/conventions/js.adoc[]
include::snippets/mediawiki/conventions/css.adoc[]
```

## Node.js snippets

| v1 path | v2 path |
|---|---|
| `snippets/nodejs/coding-conventions.adoc` | _(aggregator removed — include conventions individually)_ |
| `snippets/nodejs/coding-conventions-js.adoc` | `snippets/nodejs/conventions/js.adoc` |
| `snippets/nodejs/ci-npm.adoc` | `snippets/nodejs/execution/run-npm.adoc` |
| `snippets/nodejs/ci-mocha.adoc` | `snippets/nodejs/execution/run-tests-mocha.adoc` |
| `snippets/nodejs/ci-publish.adoc` | `snippets/nodejs/execution/publish.adoc` |

**`coding-conventions.adoc` (aggregator) was removed.** Replace with:

```adoc
include::snippets/universal/conventions/general.adoc[]
include::snippets/nodejs/conventions/general.adoc[]
include::snippets/nodejs/conventions/js.adoc[]
```

## Ansible snippets

| v1 path | v2 path |
|---|---|
| `snippets/ansible/coding-conventions.adoc` | _(aggregator removed — include conventions individually)_ |
| `snippets/ansible/coding-conventions-ansible.adoc` | `snippets/ansible/conventions/ansible.adoc` |
| `snippets/ansible/coding-conventions-molecule.adoc` | `snippets/ansible/conventions/molecule.adoc` |
| `snippets/ansible/coding-conventions-yaml.adoc` | `snippets/ansible/conventions/yaml.adoc` |

**`coding-conventions.adoc` (aggregator) was removed.** Replace with:

```adoc
include::snippets/universal/conventions/general.adoc[]
include::snippets/ansible/conventions/general.adoc[]
include::snippets/ansible/conventions/yaml.adoc[]
include::snippets/ansible/conventions/ansible.adoc[]
include::snippets/ansible/conventions/molecule.adoc[]
```
