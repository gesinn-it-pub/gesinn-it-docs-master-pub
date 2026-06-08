#!/usr/bin/env bash
# Lint AsciiDoc source files for inline markup patterns that produce invalid DocBook XML.
# Run before every commit: bash scripts/lint-adoc.sh
set -euo pipefail

ERRORS=0
SOURCES=$(find sections documents snippets -name "*.adoc" | sort)
[ -f AGENTS-source.adoc ] && SOURCES="$SOURCES AGENTS-source.adoc"
[ -f README-source.adoc ]  && SOURCES="$SOURCES README-source.adoc"

# Strip listing blocks (---- delimited) before checking — code examples may
# intentionally demonstrate the wrong patterns.
strip_listing_blocks() {
  perl -0pe 's/^----\n.*?^----\n//msg'
}

check() {
  local description="$1"
  local pattern="$2"
  local hits=""
  for f in $SOURCES; do
    local matches
    matches=$(strip_listing_blocks < "$f" | grep -Pn "$pattern" 2>/dev/null || true)
    if [ -n "$matches" ]; then
      hits="${hits}${f}:${matches}"$'\n'
    fi
  done
  if [ -n "$hits" ]; then
    printf 'FAIL: %s\n%s\n' "$description" "$hits"
    ERRORS=$((ERRORS + 1))
  fi
}

# Double asterisk inside backtick monospace span.
# ** is unconstrained bold — it opens/closes regardless of surrounding backticks,
# producing interleaved <emphasis>/<literal> DocBook tags.
# Fix: replace `glob/**` with +glob/**+ (inline passthrough).
check \
  '** inside backtick span (use +...+ passthrough instead)' \
  '`[^`\n]*\*\*[^`\n]*`'

# Single asterisk as the first character inside a backtick span.
# May initiate a bold span that outlives the monospace span.
# Fix: use +*content+ or +*content*+ instead of `*content`.
check \
  '* as first character in backtick span (use +*...+ passthrough instead)' \
  '`\*[^*`\n]'

# Single asterisk as the last character inside a backtick span.
# May close a bold span that was opened outside the monospace span.
# Fix: use +content*+ instead of `content*`.
check \
  '* as last character in backtick span (use +...*+ passthrough instead)' \
  '[^*`\n]\*`'

if [ "$ERRORS" -eq 0 ]; then
  echo "adoc-lint: OK"
  exit 0
fi

echo "${ERRORS} issue(s) found. Fix before committing."
exit 1
