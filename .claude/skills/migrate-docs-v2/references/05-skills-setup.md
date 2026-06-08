# Skills Setup

Skills are generated from the submodule's manifests at build time in each
consuming repo. The submodule provides only source files — no pre-built skills.

## Principle

```
docs/gesinn-it-docs-master-pub/
  skills/manifests/   ← source: manifest definitions
  snippets/           ← source: AsciiDoc content
  scripts/build-skills.py  ← tool: builds skills from sources

.claude/skills/       ← generated: built by CI, committed to THIS repo
.agents/skills/       ← generated: built by CI, committed to THIS repo
```

## CI step to add to build-docs.yml

Add this step before the final commit, after all other build steps:

```yaml
      # --- Skills ---

      - name: Build skills
        run: |
          PROJECT_TYPE=$(grep ':project_type:' docs/attributes.adoc | sed 's/.*: *//')
          python3 docs/gesinn-it-docs-master-pub/scripts/build-skills.py \
            --manifests-dir docs/gesinn-it-docs-master-pub/skills/manifests \
            --snippets-dir  docs/gesinn-it-docs-master-pub/snippets \
            --claude-skills-dir .claude/skills \
            --agents-skills-dir .agents/skills \
            --scope "$PROJECT_TYPE"
```

Then add `.claude/skills/` and `.agents/skills/` to the commit step's `add:` list:

```yaml
      - name: Commit generated files
        uses: EndBug/add-and-commit@v10
        with:
          add: |
            README.adoc
            docs/CONTRIBUTING.adoc
            AGENTS.md
            .claude/skills/
            .agents/skills/
```

Also add `skills/manifests/**` to the workflow trigger paths so the skills
are rebuilt when the submodule's manifests change:

```yaml
on:
  push:
    paths:
      - README-source.adoc
      - docs/CONTRIBUTING-source.adoc
      - AGENTS-source.adoc
      - docs/attributes.adoc
      - docs/gesinn-it-docs-master-pub
      - docs/gesinn-it-docs-master-pub/**
```

The `docs/gesinn-it-docs-master-pub/**` glob already covers manifest changes
since manifests live inside the submodule directory.

## What controls which skills are built

The `--scope` argument filters manifests by name substring. It is populated
from `:project_type:` in `docs/attributes.adoc`:

- `:project_type: mediawiki` → builds all skills containing `mediawiki`
  (e.g. `code-fix-php-mediawiki`, `code-write-js-mediawiki`, ...)
- `:project_type: nodejs` → builds all skills containing `nodejs`

Set `:project_type:` accurately in `docs/attributes.adoc` — it drives both
the CONTRIBUTING template selection and the skills scope.

## python3-yaml dependency

The `build-skills.py` script requires the `python3-yaml` package.
Ensure it is installed in the CI `Install tools` step:

```yaml
      - name: Install tools
        run: |
          sudo apt-get update
          sudo apt-get install -y asciidoctor pandoc python3-yaml
          sudo gem install asciidoctor-reducer --pre
```
