# Slim AGENTS-source.adoc

After path migration, `AGENTS-source.adoc` typically includes shared boilerplate
snippets (procedures, conventions, test-workflow commands) that now duplicate what
the skills provide. Remove them so that AGENTS.md stays lean.

## Rule

**AGENTS.md = project-specific rules only.**
Conventions and procedures live in `.claude/skills/` and are loaded on demand.

## What to remove

Remove any `include::` directives that pull in shared snippets:

```
# Coding Procedure — remove all four:
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/code-write.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/code-fix.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/code-refactor.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/universal/procedures/test-write.adoc[]

# Coding Conventions — remove all:
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/conventions/general.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/php/conventions/php.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/conventions/php.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/php/conventions/phan.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/conventions/js.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/conventions/css.adoc[]

# Test Workflow — remove shared snippets:
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/procedures/test-write-php-mediawiki.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/execution/install-deps.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/execution/run-tests-phpunit.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/execution/run-phan.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/execution/run-tests-npm.adoc[]
include::docs/gesinn-it-docs-master-pub/snippets/mediawiki/execution/run-pre-commit.adoc[]
```

## What to keep

- Project-specific notes (architecture decisions, dropped features, known issues)
- Project-specific test instructions (local Docker workflow, coverage commands)
- Project-specific version-compatibility notes
- The `== Conventional Commits` and `== Versioning` sections (policy, not conventions)
- Any section heading that has NO shared snippet includes beneath it

## Result

The `== Coding Procedure` and `== Coding Conventions` sections are removed entirely.
The `== Test Workflow` section keeps only project-specific content (e.g.
custom `make` targets, volume-mount notes) — remove its shared snippet includes.
