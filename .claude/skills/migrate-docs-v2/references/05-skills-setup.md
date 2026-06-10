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

## CI steps to add to build-docs.yml

Add these steps before the final commit, after the AGENTS build steps:

```yaml
      - name: Create CLAUDE.md from AGENTS.md
        run: cp AGENTS.md .claude/CLAUDE.md

      # --- Instructions ---

      - name: Create output directories
        run: |
          mkdir -p .github/instructions
          mkdir -p src libs tests .github

      - name: Build instructions (scope loop)
        shell: bash
        run: |
          BASE="docs/gesinn-it-docs-master-pub/documents/mediawiki/instructions"

          declare -A APPLY_TO=(
            [php]="**/*.php"
            [js]="**/*.{js,css,less}"
            [testing]="tests/**"
            [ci]=".github/**,Makefile,build/**"
          )

          declare -A SUBTREE_DIR=(
            [php]="src"
            [js]="libs"
            [testing]="tests"
            [ci]=".github"
          )

          for SCOPE in php js testing ci; do
            APPLYTO="${APPLY_TO[$SCOPE]}"
            DIR="${SUBTREE_DIR[$SCOPE]}"

            asciidoctor-reducer \
              -a phan \
              -o /tmp/${SCOPE}.adoc \
              ${BASE}/${SCOPE}.adoc

            asciidoctor \
              -b docbook5 \
              -o /tmp/${SCOPE}.xml \
              /tmp/${SCOPE}.adoc

            pandoc \
              -f docbook \
              -t gfm \
              /tmp/${SCOPE}.xml \
              -o /tmp/${SCOPE}.md

            printf '%s\n%s\n%s\n%s\n\n' \
              '---' \
              "applyTo: \"${APPLYTO}\"" \
              '---' \
              "<!-- AUTO-GENERATED from docs/gesinn-it-docs-master-pub/documents/mediawiki/instructions/${SCOPE}.adoc -->" \
              | cat - /tmp/${SCOPE}.md \
              > .github/instructions/${SCOPE}.instructions.md

            printf '%s\n\n' \
              "<!-- AUTO-GENERATED from docs/gesinn-it-docs-master-pub/documents/mediawiki/instructions/${SCOPE}.adoc -->" \
              | cat - /tmp/${SCOPE}.md \
              > ${DIR}/AGENTS.md
          done

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

Then update the commit step to `@v10` and include all generated files:

```yaml
      - name: Commit generated files
        uses: EndBug/add-and-commit@v10
        with:
          add: |
            README.adoc
            docs/CONTRIBUTING.adoc
            AGENTS.md
            .claude/CLAUDE.md
            .github/instructions/
            .github/AGENTS.md
            src/AGENTS.md
            libs/AGENTS.md
            tests/AGENTS.md
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

**Note on `-a phan`**: The instructions build passes `-a phan` to
`asciidoctor-reducer`. This activates Phan-specific content in repos where
`:phan:` is set in `docs/attributes.adoc`. It is harmless in repos without
Phan — the attribute simply has no effect if no conditional blocks reference it.

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
