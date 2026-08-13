<!-- THIS FILE IS AUTO-GENERATED. Edit AGENTS-source.adoc instead. -->

# Framework Structure

This is `gesinn-it-docs-master-pub` — a shared documentation library
included as a Git submodule in consumer repositories.

Three content levels:

- `snippets/` — atomic blocks, no heading, inline-embeddable

- `sections/` — standalone sections with a `==` heading (Level 2)

- `documents/` — full document templates that assemble sections and
  snippets

Scope folders: `universal/`, `mediawiki/`, `nodejs/`, `ansible/`,
`php/`, `framework/`

# Task & Skill Taxonomy

Canonical naming reference for the framework’s task and skill system.
Defines identifiers, notation conventions, folder structures, and
composition patterns.

## Naming Schema

Every task is identified by a qualified name of up to four dimensions:

    {domain}:{action}[:{language}][:{platform}]

| Dimension  | Required    | Description                                                                            |
|------------|-------------|----------------------------------------------------------------------------------------|
| `domain`   | Yes         | Subject area of the task (`code`, `test`, `lint`, …)                                   |
| `action`   | Yes         | Verb describing what is done (`write`, `fix`, `run`, …)                                |
| `language` | Conditional | Programming language (`php`, `js`, `css`, …) — omitted for language-agnostic tasks     |
| `platform` | Conditional | Framework or platform (`mediawiki`, `nodejs`, `ansible`) — omitted for universal tasks |

## Notation Conventions

Two parallel notations with a trivial bijective mapping:

| Context                                          | Separator | Example                    |
|--------------------------------------------------|-----------|----------------------------|
| Conceptual (documentation, matrices, discussion) | `:`       | `test:write:php:mediawiki` |
| File system (file names, folder names)           | `-`       | `test-write-php-mediawiki` |
| Skill `name` field (SKILL.md frontmatter)        | `-`       | `test-write-php-mediawiki` |

Mapping rule: `:` ↔ `-` — bijective, lossless.

The agentskills.io specification requires skill `name` values to contain
only lowercase letters, numbers, and hyphens. Colons are illegal in file
and folder names on Windows.

## Domains and Actions

### Action Vocabulary

| Action     | Meaning                                                              | Applicable domains     |
|------------|----------------------------------------------------------------------|------------------------|
| `write`    | Author something new                                                 | `code`, `test`, `doc`  |
| `fix`      | Correct something existing                                           | `code`, `test`, `lint` |
| `refactor` | Restructure without changing behaviour                               | `code`                 |
| `run`      | Execute and report result                                            | `test`, `lint`         |
| `update`   | Upgrade to a newer version — pipeline with optional downstream steps | `dep`                  |
| `do`       | Full cycle: prepare → human review gate → execute                    | `commit`, `release`    |

### Domain × Action Matrix

| Domain    | `write` | `fix` | `refactor` | `run` | `update` | `do` |
|-----------|---------|-------|------------|-------|----------|------|
| `code`    | ✅      | ✅    | ✅         | —     | —        | —    |
| `test`    | ✅      | ✅    | —          | ✅    | —        | —    |
| `lint`    | —       | ✅    | —          | ✅    | —        | —    |
| `doc`     | ✅      | —     | —          | —     | —        | —    |
| `dep`     | —       | —     | —          | —     | ✅       | —    |
| `commit`  | —       | —     | —          | —     | —        | ✅   |
| `release` | —       | —     | —          | —     | —        | ✅   |

### Domain Notes

`code`  
Production source code. `write` = new functionality — maps to CC type
`feat`. `fix` = bug correction — CC `fix`. `refactor` = structural
improvement without behaviour change — CC `refactor`.

`test`  
Test code only. `write` = new tests for untested or specified behaviour.
`fix` = repair failing or outdated tests. `run` = execute test suite and
report result.

`lint`  
Static analysis and style checking. `fix` = resolve a reported
violation. `run` = execute linter and report.

`doc`  
Documentation. `write` = author or update documentation.

`dep`  
Dependency management. `update` is a pipeline: update manifest → install
→ `test:run` + `lint:run` → optional `commit:do` → optional
`release:do`.

`commit`  
Commit authoring. `do` = full cycle: classify changes, compose message
(Conventional Commits format), await human approval, execute
`git commit`.

`release`  
Release preparation. `do` = full cycle: determine semver increment,
write changelog, bump version, await human approval, execute.

## Language Qualifiers

| Qualifier | Language          | Active platforms                                                             |
|-----------|-------------------|------------------------------------------------------------------------------|
| `php`     | PHP               | `mediawiki`                                                                  |
| `js`      | JavaScript        | `mediawiki`, `nodejs`                                                        |
| `css`     | CSS / LESS        | `mediawiki`                                                                  |
| `ts`      | TypeScript        | *(reserved — not yet active)*                                                |
| `yaml`    | YAML              | `ansible`                                                                    |
| *(none)*  | Language-agnostic | `test:run`, `lint:run`, `commit:do`, `release:do`, `dep:update`, `doc:write` |

## Platform Qualifiers

| Qualifier   | Platform / Framework            | Languages          |
|-------------|---------------------------------|--------------------|
| `mediawiki` | MediaWiki extension             | `php`, `js`, `css` |
| `nodejs`    | Node.js application             | `js`, `ts`         |
| `ansible`   | Ansible role                    | `yaml`             |
| *(none)*    | Universal — no platform context | —                  |

## Valid Qualified Names

Only combinations that reflect real-world development contexts are
defined. Invalid combinations (e.g. `code:write:php:nodejs`) are not
instantiated.

### `code` domain

| Qualified name                | Description                                                     |
|-------------------------------|-----------------------------------------------------------------|
| `code:write:php:mediawiki`    | Implement new PHP functionality in a MediaWiki extension        |
| `code:write:js:mediawiki`     | Implement new JavaScript functionality in a MediaWiki extension |
| `code:write:css:mediawiki`    | Implement new CSS/LESS styling in a MediaWiki extension         |
| `code:write:js:nodejs`        | Implement new JavaScript functionality in a Node.js application |
| `code:fix:php:mediawiki`      | Fix a PHP bug in a MediaWiki extension                          |
| `code:fix:js:mediawiki`       | Fix a JavaScript bug in a MediaWiki extension                   |
| `code:fix:css:mediawiki`      | Fix a CSS/LESS issue in a MediaWiki extension                   |
| `code:fix:js:nodejs`          | Fix a JavaScript bug in a Node.js application                   |
| `code:refactor:php:mediawiki` | Refactor PHP code in a MediaWiki extension                      |
| `code:refactor:js:mediawiki`  | Refactor JavaScript code in a MediaWiki extension               |
| `code:refactor:js:nodejs`     | Refactor JavaScript code in a Node.js application               |

### `test` domain

| Qualified name             | Description                                           |
|----------------------------|-------------------------------------------------------|
| `test:write:php:mediawiki` | Write PHPUnit / MediaWiki test-case tests             |
| `test:write:js:mediawiki`  | Write QUnit tests for a MediaWiki extension           |
| `test:write:js:nodejs`     | Write Mocha / Jest tests for a Node.js application    |
| `test:fix:php:mediawiki`   | Repair failing PHPUnit tests in a MediaWiki extension |
| `test:fix:js:mediawiki`    | Repair failing QUnit tests in a MediaWiki extension   |
| `test:fix:js:nodejs`       | Repair failing JS tests in a Node.js application      |
| `test:run:mediawiki`       | Run the full test suite for a MediaWiki extension     |
| `test:run:nodejs`          | Run the full test suite for a Node.js application     |

### `lint` domain

| Qualified name           | Description                                          |
|--------------------------|------------------------------------------------------|
| `lint:fix:php:mediawiki` | Fix PHPCS / Phan violations in a MediaWiki extension |
| `lint:fix:js:mediawiki`  | Fix ESLint violations in a MediaWiki extension       |
| `lint:fix:css:mediawiki` | Fix stylelint violations in a MediaWiki extension    |
| `lint:fix:js:nodejs`     | Fix ESLint violations in a Node.js application       |
| `lint:run:mediawiki`     | Run all linters for a MediaWiki extension            |
| `lint:run:nodejs`        | Run all linters for a Node.js application            |

### Language-agnostic tasks

| Qualified name         | Description                                                 |
|------------------------|-------------------------------------------------------------|
| `doc:write`            | Write or update documentation                               |
| `dep:update:mediawiki` | Update Composer dependencies in a MediaWiki extension       |
| `dep:update:nodejs`    | Update npm dependencies in a Node.js application            |
| `commit:do`            | Classify changes, compose and execute a Conventional Commit |
| `release:do`           | Prepare and execute a versioned release                     |

## Conventional Commits Mapping

Task identifiers and Conventional Commits types serve different purposes
in separate namespaces. The mapping is applied operationally in the
`commit:do` skill.

| Task (agent instruction namespace) | CC type (commit message namespace)             |
|------------------------------------|------------------------------------------------|
| `code:write`                       | `feat`                                         |
| `code:fix`                         | `fix`                                          |
| `code:refactor`                    | `refactor`                                     |
| `test:write`                       | `test`                                         |
| `test:fix`                         | `test`                                         |
| `lint:fix`                         | `style` or `fix` (depending on violation type) |
| `doc:write`                        | `docs`                                         |
| `dep:update`                       | `chore(deps)`                                  |
| `release:do`                       | `chore(release)`                               |

## Snippet Folder Structure (Canonical)

Snippets are the single source of truth (SPoT). Skills and AGENTS.md
files are build outputs assembled from snippets at build time.

    snippets/
      universal/
        conventions/
          general.adoc
        procedures/
          code-write.adoc           # procedure: TDD — test-first, then implement
          code-fix.adoc             # procedure: reproduce-first
          code-refactor.adoc        # procedure: safety-net (green before and after)
          test-write.adoc           # procedure: spec-first, universal
      php/                          # new scope: PHP-specific, platform-independent
        conventions/
          php.adoc
          phan.adoc
        procedures/
          test-write-php.adoc       # delta: PHPUnit conventions
      mediawiki/
        conventions/
          general.adoc              # was: coding-conventions-general.adoc
          php.adoc                  # was: coding-conventions-php.adoc (MW delta over php/)
          js.adoc                   # was: coding-conventions-js.adoc
          css.adoc                  # was: coding-conventions-css.adoc
        procedures/
          test-write-php-mediawiki.adoc  # delta: MW base classes, runner (replaces test-first-approach.adoc)
        execution/
          run-tests-phpunit.adoc    # was: ci-phpunit.adoc
          run-tests-npm.adoc        # was: ci-npm.adoc
          run-phan.adoc             # was: ci-phan.adoc
          run-pre-commit.adoc       # was: ci-pre-commit.adoc
          install-deps.adoc         # was: ci-install.adoc
      nodejs/
        conventions/
          …
      ansible/
        conventions/
          …

Each layer contains **only the delta** over the layer below — no
repetition of content already defined at a higher abstraction level.

## Snippet Heading Convention

Every snippet file must open with a bold title that follows this
pattern:

    *{Category} — {Content} [· {Scope}]*

| Placeholder  | Meaning                                                                                       | Values                                                                  |
|--------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| `{Category}` | The type of content in this snippet                                                           | `Coding Conventions`, `Procedure`, `Execution`, `Static Analysis`       |
| `{Content}`  | The subject — the task name (`code:write`), the technology (`PHP`), or the topic (`Baseline`) | Free text, title-cased                                                  |
| `· {Scope}`  | Optional scope qualifier, prefixed with the middle dot `·` (U+00B7)                           | Language (`PHP`, `Node.js`), platform (`MediaWiki`, `Ansible`), or both |

The `·` scope qualifier is omitted when the snippet is universal (no
language or platform restriction).

Examples:

| Title                                           | Snippet                                                             |
|-------------------------------------------------|---------------------------------------------------------------------|
| \*Coding Conventions — Baseline\*               | `universal/conventions/general.adoc` — no scope qualifier           |
| \*Coding Conventions — PHP · MediaWiki\*        | `mediawiki/conventions/php.adoc` — MW delta over the base PHP layer |
| \*Procedure — code:write\*                      | `universal/procedures/code-write.adoc` — universal, no qualifier    |
| \*Procedure — test:write · PHP\*                | `php/procedures/test-write-php.adoc` — PHP-scoped procedure         |
| \*Execution — Run Tests (PHPUnit) · MediaWiki\* | `mediawiki/execution/run-tests-phpunit.adoc`                        |
| \*Static Analysis — Phan · PHP\*                | `php/conventions/phan.adoc`                                         |

## Skill Structure

Skills are generated into `.claude/skills/` (Claude Code) and
`.agents/skills/` (VS Code Copilot and other agentskills.io-compatible
clients).

    .claude/skills/
      {skill-name}/
        SKILL.md                   # frontmatter + body (< 500 lines recommended)
        references/
          NN-{snippet-name}.md    # rendered snippets, numbered for load order

Each skill is **self-contained** at runtime — no dependency on other
skills. The same snippet source may appear in multiple skills'
`references/` folders. SPoT is maintained at the AsciiDoc source level;
output duplication is accepted.

Skills correspond to BPMN **Processes**: each skill orchestrates a
complete workflow. Snippets in `references/` correspond to BPMN
**Tasks**: reusable steps within a process.

### Example: `code-write-php-mediawiki`

    .claude/skills/code-write-php-mediawiki/
      SKILL.md
      references/
        01-code-write.md                 # from universal/procedures/code-write.adoc
        02-conventions-general.md        # from mediawiki/conventions/general.adoc
        03-conventions-php.md            # from php/conventions/php.adoc
        04-conventions-phan.md           # from php/conventions/phan.adoc
        05-conventions-php-mediawiki.md  # from mediawiki/conventions/php.adoc
        06-test-write.md                 # from universal/procedures/test-write.adoc
        07-test-write-php.md             # from php/procedures/test-write-php.adoc
        08-test-write-php-mediawiki.md   # from mediawiki/procedures/test-write-php-mediawiki.adoc
        09-run-tests-phpunit.md          # from mediawiki/execution/run-tests-phpunit.adoc
        10-run-pre-commit.md             # from mediawiki/execution/run-pre-commit.adoc

## Composition Manifests

Each skill is described by a YAML composition manifest that drives the
build. Manifests live in `skills/manifests/` and are the
machine-readable equivalent of the Task × Rule-sets Matrix.

``` yaml
# skills/manifests/code-write-php-mediawiki.yml
skill: code-write-php-mediawiki
description: >
  Implement new PHP functionality in a MediaWiki extension.
  Use when asked to add a new feature, implement a method,
  or build new behaviour in PHP within a MediaWiki context.
references:
  - universal/procedures/code-write.adoc
  - mediawiki/conventions/general.adoc
  - php/conventions/php.adoc
  - php/conventions/phan.adoc
  - mediawiki/conventions/php.adoc
  - universal/procedures/test-write.adoc
  - php/procedures/test-write-php.adoc
  - mediawiki/procedures/test-write-php-mediawiki.adoc
  - mediawiki/execution/run-tests-phpunit.adoc
  - mediawiki/execution/run-pre-commit.adoc
```

## Existing File Migration

| Current path                                         | Canonical path                                                                                      | Action                                             |
|------------------------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------|
| `snippets/universal/coding-procedure.adoc`           | `universal/procedures/code-write.adoc` + `code-fix.adoc` + `code-refactor.adoc` + `test-write.adoc` | Split                                              |
| `snippets/mediawiki/test-first-approach.adoc`        | `mediawiki/procedures/test-write-php-mediawiki.adoc`                                                | Rename + extend                                    |
| `snippets/mediawiki/coding-conventions-general.adoc` | `mediawiki/conventions/general.adoc`                                                                | Rename                                             |
| `snippets/mediawiki/coding-conventions-php.adoc`     | PHP layer → `php/conventions/php.adoc`; MW delta → `mediawiki/conventions/php.adoc`                 | Split + move                                       |
| `snippets/mediawiki/coding-conventions-js.adoc`      | `mediawiki/conventions/js.adoc`                                                                     | Rename                                             |
| `snippets/mediawiki/coding-conventions-css.adoc`     | `mediawiki/conventions/css.adoc`                                                                    | Rename                                             |
| `snippets/mediawiki/coding-conventions-phan.adoc`    | `php/conventions/phan.adoc`                                                                         | Move + rename (Phan is PHP-layer, not MW-specific) |
| `snippets/mediawiki/ci-phpunit.adoc`                 | `mediawiki/execution/run-tests-phpunit.adoc`                                                        | Rename                                             |
| `snippets/mediawiki/ci-npm.adoc`                     | `mediawiki/execution/run-tests-npm.adoc`                                                            | Rename                                             |
| `snippets/mediawiki/ci-phan.adoc`                    | `mediawiki/execution/run-phan.adoc`                                                                 | Rename                                             |
| `snippets/mediawiki/ci-pre-commit.adoc`              | `mediawiki/execution/run-pre-commit.adoc`                                                           | Rename                                             |
| `snippets/mediawiki/ci-install.adoc`                 | `mediawiki/execution/install-deps.adoc`                                                             | Rename                                             |

## Agent Skills Format Reference

Key facts about the Agent Skills format — available here without web
lookup. Source: <https://agentskills.io> /
[agentskills/agentskills](https://github.com/agentskills/agentskills)

### What Are Agent Skills?

A lightweight, open format originally developed by Anthropic and
released as an open standard. A skill is a folder containing a
`SKILL.md` file with YAML frontmatter and Markdown body. Supported by
Claude Code, VS Code Copilot, and other agentskills.io-compatible
clients.

### Progressive Disclosure

Skills load in three stages — full instructions only when needed:

| Stage      | Context cost                | What is loaded                                                                      |
|------------|-----------------------------|-------------------------------------------------------------------------------------|
| Discovery  | ~100 tokens per skill       | `name` + `description` only — at startup, for all available skills                  |
| Activation | \< 5 000 tokens recommended | Full `SKILL.md` body — when task matches the description                            |
| Execution  | On demand                   | Files in `references/`, `scripts/`, `assets/` — when the skill body references them |

### `SKILL.md` Frontmatter Fields

| Field           | Required | Description                                                                                        |
|-----------------|----------|----------------------------------------------------------------------------------------------------|
| `name`          | Yes      | Max 64 chars. Lowercase letters, numbers, hyphens only. Must match folder name.                    |
| `description`   | Yes      | Max 1 024 chars. Describes what the skill does and **when to use it**. Primary activation trigger. |
| `license`       | No       | License name or reference to a bundled license file.                                               |
| `compatibility` | No       | Max 500 chars. Environment requirements (OS, installed tools, network access).                     |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                               |
| `allowed-tools` | No       | Space-separated pre-approved tools the skill may use. *(Experimental)*                             |

### Key Design Principles

- Keep `SKILL.md` under 500 lines / 5 000 tokens — the body loads in
  full on activation.

- Move detailed reference material to `references/` and instruct the
  agent **when** to load each file.

- The `description` field is the sole activation trigger — write it to
  match the right prompts and reject near-misses.

- Add only what the agent **would not know without the skill**: project
  conventions, non-obvious edge cases, specific tool commands.

- Favour procedures over declarations: teach the agent how to approach a
  class of problems, not what to produce for a specific instance.

# Build System

`scripts/build-skills.py` assembles skills from YAML manifests and
AsciiDoc snippets. The script is the single source of truth for the
generated output structure. CI runs it on every push that touches
snippets/\*\* or skills/manifests/\*\*.

**The build never runs locally in this repository.** It executes
exclusively in the CI pipelines of consumer repositories. Do not attempt
to run `scripts/build-skills.py` or any related build command locally —
the required toolchain (`asciidoctor-reducer`, `pandoc`, etc.) is not
installed here and local execution is forbidden.

## Build Invariants

These invariants must hold after every successful build. Violations
indicate either a manifest error or a bug in the build script.

### Idempotency

Running the build twice in a row must produce identical output. The
script achieves this by deleting all \*.md files from each skill’s
`references/` directory before writing new ones.

**Corollary:** Never hand-edit files inside `.claude/skills/` or
`.agents/skills/` — they are fully owned by the build and will be
overwritten on the next CI run.

### Output Filename Uniqueness

Each entry in a manifest must map to a distinct output filename within
that skill’s `references/` directory.

Output filenames follow the pattern:

    {NN}-{scope}-{name}.md

where `{scope}` is the first path component of the snippet (e.g.
`universal`, `php`, `mediawiki`) and `{name}` is the basename without
extension.

Example: `php/conventions/php.adoc` and `mediawiki/conventions/php.adoc`
both have basename `php.adoc` but produce distinct files `02-php-php.md`
and `05-mediawiki-php.md`.

**Rule:** A manifest must never reference two snippets from the same
scope with the same basename. Such a collision would indicate a content
design error — two files in the same scope doing the same job.

### Reference Count Consistency

The number of \*.md files in a skill’s `references/` directory must
equal the number of entries in its manifest. A higher count indicates
stale files that were not cleaned; a lower count indicates a missing or
unresolvable snippet.

### No Duplicate Top-Level Titles

The first bold line of each snippet is its identifier title (e.g.
\*Coding Conventions — PHP · MediaWiki\*). Each identifier title must
appear exactly once across a skill’s assembled reference files. A
duplicate identifier title means two snippets cover the same topic — a
violation of the delta principle.

Internal subheadings within a snippet (e.g. \*Naming\*,
\*Architecture\*) are scoped to their snippet and may share names across
different snippets in the same skill, as long as their content is
additive and non-overlapping.

The delta principle: each snippet layer adds only what is not already
defined at a higher abstraction level. For example, a MediaWiki skill
includes `mediawiki/conventions/general.adoc` (the complete MW baseline)
but **not** `universal/conventions/general.adoc` (which is a strict
subset of the MW baseline).

## Manifest Authoring Rules

When adding or modifying a `skills/manifests/*.yml` file:

1.  List snippets from most general to most specific — universal before
    platform-specific.

2.  Do not include a snippet if its content is already fully covered by
    another snippet in the same manifest.

3.  Do not include two snippets from the same scope that share a
    basename — rename one of the source files instead.

4.  Validate by verifying that the number of entries in the manifest
    matches the expected reference count — the build itself runs in CI
    only.

# AsciiDoc Authoring Conventions

Rules for writing AsciiDoc source files in this repository. Violations
are caught by `scripts/lint-adoc.sh`, which runs as the first step in CI
and as a local pre-commit hook.

**One-time setup per clone** — activates the pre-commit hook:

``` console
git config core.hooksPath .githooks
```

After that, `scripts/lint-adoc.sh` runs automatically on every
`git commit`. To run manually at any time:

``` console
bash scripts/lint-adoc.sh
```

## Inline Markup Rules

These rules prevent invalid DocBook XML during the AsciiDoc → DocBook →
Markdown conversion pipeline.

### No double asterisk inside backtick spans

Double asterisk (\*\*) is an **unconstrained** bold marker — it opens
and closes regardless of surrounding formatting spans, including
backtick monospace. When \*\* appears inside a backtick span it leaks
out, producing interleaved `<emphasis>` and `<literal>` DocBook tags.

<div class="formalpara-title">

**Wrong — causes invalid DocBook**

</div>

    CI runs on every push to `snippets/**`.

<div class="formalpara-title">

**Correct — use inline passthrough**

</div>

    CI runs on every push to +snippets/**+.

### No `*` as first or last character inside a backtick span

A single asterisk at the very start or end of a backtick span may be
parsed as a constrained bold delimiter, producing the same interleaved
DocBook output.

<div class="formalpara-title">

**Wrong — asterisk at start or end of backtick span**

</div>

    Exclude `*.log` files.
    Multiple `assert*` calls are fine.

<div class="formalpara-title">

**Correct — use inline passthrough**

</div>

    Exclude +*.log+ files.
    Multiple +assert*+ calls are fine.

### Rule of thumb

When displaying text that contains `*` in a monospace context, always
use the inline passthrough `...` instead of backtick monospace. Backtick
spans are safe only when the content contains no asterisks.

### Bold titles in snippet files

Snippet files open with a bold title using the `*Title Text*` pattern
written as plain AsciiDoc bold (not inside backticks). When referencing
these titles in prose, use the inline passthrough `*...*` rather than
wrapping in backtick monospace.

# Commit Convention

## Conventional Commits Policy

**Commit Convention — Conventional Commits**

Commit messages follow the [Conventional Commits
specification](https://www.conventionalcommits.org/).

Commit format:

`type(scope): short description`

The scope is optional and should describe the affected subsystem,
module, or dependency when useful.

Examples:

- feat(api): add autocomplete endpoint

- fix(parser): handle empty token lists

- docs(readme): explain input architecture

- refactor(parser): simplify token parsing

- deps(smw): bump from 5.1.0 to 5.2.0

- ci(github): update workflow configuration

- test(api): add autocomplete tests

Recommended commit types:

- `feat` — new functionality

- `fix` — bug fixes

- `deps` — dependency updates

- `docs` — documentation changes

- `refactor` — internal code changes without behavioral change

- `test` — tests added or updated

- `ci` — changes to continuous integration configuration

- `chore` — repository maintenance tasks without impact on runtime
  behavior

Dependency updates:

- Use the `deps` type for dependency upgrades

- The scope should identify the dependency being updated

- Include the version change when applicable

Example:

- deps(smw): bump from 5.1.0 to 5.2.0

Guidelines:

- Use the imperative mood (e.g. "add feature", not "added feature")

- Keep the subject line concise

- Use the commit body to explain **why**, not only **what**

- Scopes should be short, lowercase identifiers (e.g. `api`, `parser`,
  `smw`, `mediawiki`, `docker`)

- Use `chore` only for repository maintenance tasks that do not affect
  runtime behavior, dependencies, CI configuration, or tests

- Do **not** add a `Co-Authored-By:` trailer or any agent attribution
  line to the commit message

Changelog:

- After committing a `feat`, `fix`, `deps`, `refactor`, or `docs`
  change, add a corresponding entry to the `[Unreleased]` section of
  `CHANGELOG.md` — do not wait until release time.

# Versioning

## Versioning and Releases

**Versioning Convention — Semantic Versioning**

This project follows [Semantic Versioning](https://semver.org/).

Version numbers follow the format:

`MAJOR.MINOR.PATCH`

Version increment rules:

- MAJOR — incompatible or breaking changes

- MINOR — backwards-compatible feature additions

- PATCH — backwards-compatible bug fixes

Breaking changes include (but are not limited to):

- incompatible API changes

- removal or renaming of public interfaces

- behavior changes that may break existing integrations

- increased minimum runtime or dependency requirements

- incompatible configuration or data format changes

- dependency upgrades that introduce breaking changes for users

Breaking changes must always increment the MAJOR version.

## Changelog

**Changelog Convention**

This project maintains a `CHANGELOG.md` following [Keep a
Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow
[Semantic Versioning](https://semver.org/). Version numbers have no `v`
prefix.

**Format**

``` markdown
# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/) and
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- ...

## [1.2.0] - 2026-06-09

Adds autocomplete support and fixes parser edge cases. Removes the deprecated
`oldMethod()` API — see Breaking Changes below.

### Breaking Changes
- Remove deprecated `oldMethod()` API [`a1b2c3d`](https://github.com/org/repo/commit/a1b2c3d)

### Added
- Add autocomplete endpoint [`6e376e3`](https://github.com/org/repo/commit/6e376e3)

### Changed
- Bump dependency from 1.0.0 to 2.0.0 [`4fb2375`](https://github.com/org/repo/commit/4fb2375)
- Refactor token parser for clarity [`9a3c1f2`](https://github.com/org/repo/commit/9a3c1f2)
- Update installation documentation [`78d57e5`](https://github.com/org/repo/commit/78d57e5)

### Fixed
- Handle empty token list in parser [`43b9f08`](https://github.com/org/repo/commit/43b9f08) ([#42](https://github.com/org/repo/issues/42))

[Unreleased]: https://github.com/org/repo/compare/1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/org/repo/releases/tag/1.1.0
```

**Change categories**

Map conventional commit types to changelog categories as follows:

| Commit type                                | Changelog category              |
|--------------------------------------------|---------------------------------|
| `feat`                                     | Added                           |
| `fix`                                      | Fixed                           |
| `deps`                                     | Changed                         |
| `refactor`                                 | Changed                         |
| `docs`                                     | Changed                         |
| Breaking change (`!` or `BREAKING CHANGE`) | Breaking Changes (always first) |
| `ci`, `chore`, `test`                      | — omit from changelog           |

**Audience and tone**

Changelog entries are written for the **end user** of the software, not
for developers reading the commit history. The commit hash link already
gives access to the technical detail — the entry itself must not just
restate the commit message verbatim.

- Describe the user-visible effect or benefit, not the implementation
  step. Ask "what changes for someone using this software?", not "what
  did the commit do?".

- Keep it short and factual — one line, imperative mood, no marketing
  language.

- Avoid internal terminology (class/function/variable names, refactor
  mechanics) unless it is the actual subject of the change (e.g. a
  public API rename that affects integrators).

| Commit message (technical)                                      | Changelog entry (user-facing)                       |
|-----------------------------------------------------------------|-----------------------------------------------------|
| `fix(parser): use strict equality in isEmpty() check`           | Fix incorrect handling of empty input in the parser |
| `refactor(api): extract validateToken() into middleware`        | *(omit — no user-visible effect)*                   |
| `feat(api): add /autocomplete endpoint returning top-5 matches` | Add autocomplete suggestions while typing           |

**Rules**

- Every version has an entry — no skipped releases.

- Latest version comes first. `[Unreleased]` is always at the top.

- Each version may open with a short introductory sentence summarising
  the release theme (optional but recommended for notable releases).

- Each entry includes the short commit hash as a link, appended at the
  end of the line.

- If the change relates to a GitHub issue or PR, append the issue/PR
  link after the commit hash: `` [`commit ``\](url) (\[#42\](url))\`.

- Dates use ISO 8601 format (`YYYY-MM-DD`).

- Yanked releases are marked: `## [1.2.0] - 2026-06-09 [YANKED]`

- Compare links are maintained at the bottom of the file.

- The `[Unreleased]` section is updated continuously as notable changes
  are committed — do not wait until release time.

**Rotation at major releases**

When a new MAJOR version is released, the previous major’s history is
rotated out of `CHANGELOG.md` into a dedicated archive file:

1.  Move all entries for the previous major (e.g. all `1.x.x` sections)
    into `CHANGELOG-1.x.md`.

2.  Add a link at the bottom of `CHANGELOG.md`:

    `Older releases: [1.x](CHANGELOG-1.x.md)`

3.  `CHANGELOG.md` then contains only the current major’s releases plus
    `[Unreleased]`.

4.  Archive files are never modified after creation.

## Release Workflow

**Procedure — release:do**

1.  Never rely on `gh auth login` / `~/.config/gh/hosts.yml` for the
    `gh` calls below — that file holds a single global login that can
    silently drift from the identity this repo actually needs. Instead,
    every step in this procedure that invokes `gh` resolves the token
    live from the environment and passes it inline, in the **same**
    shell invocation as the `gh` call — a variable set in one tool call
    does not survive into a later, separate tool call, so the resolution
    must be repeated at each `gh` call site rather than hoisted into a
    one-time preflight step:

    ``` shell
    gh_user=$(git config user.name)
    env_var="GH_TOKEN_$(echo "$gh_user" | tr '[:lower:]-' '[:upper:]_')"
    token="${!env_var}"
    if [ -z "$token" ]; then
      echo "Missing $env_var for gh user '$gh_user' — set it before releasing." >&2
      exit 1
    fi
    GH_TOKEN="$token" gh ...
    ```

2.  Confirm the target branch — the tag must be created from the correct
    branch:

    - Run `git branch --show-current`.

    - For a release on `main` (normal or MAJOR): stay on `main`.

    - For a backport release on an older major (e.g. `2.4.1` while `3.x`
      is on `main`): check out the maintenance branch first
      (`git checkout 2.x`). All remaining steps — including the tag and
      GitHub release — execute on that branch.

3.  Determine the new version number from commits since the last tag
    using SemVer rules:

    - Any breaking change (`!` or `BREAKING CHANGE`) → MAJOR

    - Any `feat` commit → MINOR

    - Only `fix`, `deps`, `refactor`, `docs` commits → PATCH

4.  If this is a **MAJOR** bump (e.g. `2.x → 3.0.0`): create a
    maintenance branch for the outgoing major **before** making any
    other changes:

    ``` console
    git checkout -b N.x          # e.g. git checkout -b 2.x  (snapshot of current main)
    git push origin N.x
    git checkout main            # tag 3.0.0 will be set from main
    ```

5.  Identify the version file for this project. Common locations:

    - `package.json` (Node.js)

    - `extension.json` / `composer.json` (MediaWiki extension)

    - `composer.json` (PHP library)

    - If unclear, ask the user before proceeding.

6.  Bump the version number in the version file.

7.  Update `CHANGELOG.md`:

    - Rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD` (today’s date, ISO
      8601).

    - Add a new empty `[Unreleased]` section at the top.

    - If this is a MAJOR release: rotate the previous major’s entries
      into `CHANGELOG-PREV.x.md` and add an "Older releases" link at the
      bottom of `CHANGELOG.md` (see Changelog Convention).

    - Update the compare links at the bottom:

          [Unreleased]: https://github.com/org/repo/compare/X.Y.Z...HEAD
          [X.Y.Z]: https://github.com/org/repo/compare/PREV...X.Y.Z

8.  Draft the release notes:

    - Write a short introductory sentence summarising the release theme
      (optional but recommended for notable releases).

    - Write each entry for the **end user** — describe the user-visible
      effect, not the commit message verbatim (see Changelog Convention,
      **Audience and tone**).

    - Ensure each entry has a commit hash link; add an issue/PR link
      where applicable.

    - Present the full `[X.Y.Z]` changelog section inside a fenced
      markdown code block for easy review.

    - Do not proceed until the user explicitly approves.

9.  After approval — commit all changes:

        prepare X.Y.Z [skip ci]

10. Push the branch.

11. Create and push the git tag:

    ``` console
    git tag X.Y.Z
    git push origin X.Y.Z
    ```

12. Create the GitHub release using the approved changelog section as
    body. Resolve the token inline as shown above, in the same shell
    invocation:

    ``` shell
    gh_user=$(git config user.name)
    env_var="GH_TOKEN_$(echo "$gh_user" | tr '[:lower:]-' '[:upper:]_')"
    token="${!env_var}"
    if [ -z "$token" ]; then
      echo "Missing $env_var for gh user '$gh_user' — set it before releasing." >&2
      exit 1
    fi
    GH_TOKEN="$token" gh release create X.Y.Z --title "X.Y.Z" --notes "<approved changelog section>"
    ```
