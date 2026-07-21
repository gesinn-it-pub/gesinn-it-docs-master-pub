#!/usr/bin/env python3
"""Build Claude Code and agent skills from YAML composition manifests.

For each manifest in <manifests-dir>/*.yml:
  1. Read the skill name, description, and references list.
  2. Convert each referenced AsciiDoc snippet to Markdown.
  3. Write numbered reference files to <claude-skills-dir>/{name}/references/.
  4. Write a SKILL.md with frontmatter and a body that loads the references.

Also mirrors output to <agents-skills-dir>/{name}/ for VS Code Copilot / other agents.

NOTE: This script is NOT run by the submodule's own CI. Skills are built exclusively
by consumer repos — this script is provided for them to call. Do not add a skill-build
step to build-docs.yml.

Designed to be called from within the submodule directory or from a consumer repo
root with explicit path overrides:

  # From submodule root (default paths):
  python3 scripts/build-skills.py

  # From consumer repo root (pointing into the submodule):
  python3 docs/gesinn-it-docs-master-pub/scripts/build-skills.py \\
    --manifests-dir docs/gesinn-it-docs-master-pub/skills/manifests \\
    --snippets-dir  docs/gesinn-it-docs-master-pub/snippets \\
    --claude-skills-dir .claude/skills \\
    --agents-skills-dir .agents/skills \\
    --scope mediawiki

  # With an additional private snippets root (e.g. DOCSM) and multiple scopes:
  python3 docs/gesinn-it-docs-master-pub/scripts/build-skills.py \\
    --manifests-dir docs/gesinn-it-docs-master-pub/skills/manifests \\
    --manifests-dir docs/gesinn-it-docs-master/skills/manifests \\
    --snippets-dir  docs/gesinn-it-docs-master-pub/snippets \\
    --extra-snippets-dir docs/gesinn-it-docs-master/snippets \\
    --claude-skills-dir .claude/skills \\
    --agents-skills-dir .agents/skills \\
    --scope mediawiki \\
    --scope debug-fix-docker-mediawiki

Snippet references in manifests are resolved against --snippets-dir first,
then against each --extra-snippets-dir in order. The first match wins.
"""

import argparse
import os
import subprocess
import sys
import yaml


def adoc_to_markdown(adoc_path, attributes=None):
    """Convert an AsciiDoc file to Markdown via asciidoctor + pandoc."""
    attr_flags = []
    for attr in (attributes or []):
        attr_flags += ["-a", attr]
    try:
        reduced = subprocess.run(
            ["asciidoctor-reducer"] + attr_flags + [adoc_path],
            capture_output=True, text=True, check=True
        ).stdout

        tmp_adoc = "/tmp/skill-snippet.adoc"
        tmp_xml = "/tmp/skill-snippet.xml"
        with open(tmp_adoc, "w") as f:
            f.write(reduced)

        subprocess.run(
            ["asciidoctor", "-b", "docbook5"] + attr_flags + ["-o", tmp_xml, tmp_adoc],
            capture_output=True, text=True, check=True
        )

        result = subprocess.run(
            ["pandoc", "-f", "docbook", "-t", "gfm", tmp_xml],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"  WARNING: conversion failed for {adoc_path}: {e.stderr.strip()}", file=sys.stderr)
        with open(adoc_path) as f:
            return f.read().strip()


def platform_qualifier(skill_name, platforms):
    """Return the platform qualifier trailing skill_name, or None if it has none.

    Matches only a whole hyphen-delimited segment run at the end of the name
    (per the Naming Schema in CLAUDE.md: {domain}-{action}[-{language}][-{platform}]),
    never a bare substring — e.g. "mediawiki" must not match inside "docker-mediawiki".
    Checks longest platform names first so a compound qualifier like
    "docker-mediawiki" is found before a shorter one it contains.
    """
    for p in sorted(platforms, key=len, reverse=True):
        if skill_name == p or skill_name.endswith("-" + p):
            return p
    return None


def resolve_snippet(ref_path, snippets_dirs):
    """Find the first existing snippet file across all snippet roots."""
    for snippets_dir in snippets_dirs:
        candidate = os.path.join(snippets_dir, ref_path)
        if os.path.exists(candidate):
            return candidate
    return None


def write_skill(manifest_path, snippets_dirs, output_base_dir, attributes=None, custom_file=None):
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    skill_name = manifest["skill"]
    description = manifest["description"].strip()
    references = manifest.get("references", [])

    skill_dir = os.path.join(output_base_dir, skill_name)
    refs_dir = os.path.join(skill_dir, "references")
    os.makedirs(refs_dir, exist_ok=True)

    for stale in os.listdir(refs_dir):
        if stale.endswith(".md"):
            os.remove(os.path.join(refs_dir, stale))

    ref_lines = []
    ref_index = 0
    for ref_path in references:
        adoc_path = resolve_snippet(ref_path, snippets_dirs)
        if not adoc_path:
            print(f"  WARNING: snippet not found in any root: {ref_path}", file=sys.stderr)
            continue

        md_content = adoc_to_markdown(adoc_path, attributes)
        if not md_content.strip():
            print(f"  Skipping {ref_path} -> rendered empty (likely excluded by attributes)", file=sys.stderr)
            continue

        ref_index += 1
        parts = ref_path.replace("\\", "/").split("/")
        scope = parts[0]
        name = os.path.splitext(parts[-1])[0]
        ref_filename = f"{ref_index:02d}-{scope}-{name}.md"
        ref_filepath = os.path.join(refs_dir, ref_filename)

        print(f"  Converting {ref_path} -> references/{ref_filename}")
        with open(ref_filepath, "w") as f:
            f.write(md_content + "\n")

        ref_lines.append(f"- `references/{ref_filename}`")

    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    ref_section = "\n".join(ref_lines) if ref_lines else "_No references._"
    custom_section = ""
    if custom_file:
        custom_section = f"""
## Repo-specific conventions

Load `99-custom.md` if it exists, resolved two directories up from this
SKILL.md file (i.e. the `.claude/` or `.agents/` folder that contains this
skill's own `skills/` directory — NOT the target repo root, and NOT the
current working directory if this skill was loaded via `--add-dir` from an
external skills location). It contains project-specific rules that override
or extend the references above.
"""
    with open(skill_md_path, "w") as f:
        f.write(f"""---
name: {skill_name}
description: >
  {description}
---

Load the following reference files before starting work:

{ref_section}
{custom_section}""")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifests-dir", action="append", dest="manifests_dirs",
                        default=None,
                        help="Directory containing *.yml skill manifests. "
                             "Can be specified multiple times. (default: skills/manifests)")
    parser.add_argument("--snippets-dir", default="snippets",
                        help="Primary directory containing AsciiDoc snippets (default: snippets)")
    parser.add_argument("--extra-snippets-dir", action="append", dest="extra_snippets_dirs",
                        default=[],
                        help="Additional snippet root to search after --snippets-dir. "
                             "Can be specified multiple times.")
    parser.add_argument("--claude-skills-dir", default=".claude/skills",
                        help="Output directory for Claude Code skills (default: .claude/skills)")
    parser.add_argument("--agents-skills-dir", default=".agents/skills",
                        help="Output directory for agent skills (default: .agents/skills)")
    parser.add_argument("--scope", action="append", dest="scopes", default=None,
                        help="Only build skills whose name contains this string (e.g. 'mediawiki'). "
                             "Can be specified multiple times — a skill matches if its name contains any scope. "
                             "Skills with no platform qualifier are always built regardless of scope.")
    parser.add_argument("--platforms", default="mediawiki,nodejs,ansible,docker-mediawiki,factory",
                        help="Comma-separated list of known platform qualifiers "
                             "(default: mediawiki,nodejs,ansible,docker-mediawiki,factory). "
                             "Used to identify platform-specific skills when --scope is set.")
    parser.add_argument("--attribute", "-a", action="append", dest="attributes", default=[],
                        help="AsciiDoc attribute to set (e.g. 'phan'). "
                             "Can be specified multiple times. Passed to asciidoctor-reducer and asciidoctor.")
    parser.add_argument("--custom-file", default=None,
                        help="Path to a repo-specific 99-custom.md file. When set, every SKILL.md "
                             "gets a section instructing the agent to load ../../99-custom.md.")
    args = parser.parse_args()

    if args.manifests_dirs is None:
        args.manifests_dirs = ["skills/manifests"]

    snippets_dirs = [args.snippets_dir] + args.extra_snippets_dirs

    manifests = []
    for manifests_dir in args.manifests_dirs:
        if not os.path.isdir(manifests_dir):
            print(f"No manifests directory found at {manifests_dir} — skipping.")
            continue
        for f in sorted(os.listdir(manifests_dir)):
            if f.endswith(".yml"):
                manifests.append(os.path.join(manifests_dir, f))

    if not manifests:
        print("No manifest files found.")
        return

    if args.scopes:
        platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]
        def manifest_skill_name(manifest_path):
            return os.path.splitext(os.path.basename(manifest_path))[0]
        def matches_scope(manifest_path):
            qualifier = platform_qualifier(manifest_skill_name(manifest_path), platforms)
            return qualifier is None or qualifier in args.scopes
        manifests = [f for f in manifests if matches_scope(f)]

    if not manifests:
        print(f"No manifest files found matching scopes '{', '.join(args.scopes)}'.")
        return

    for manifest_path in manifests:
        skill_name = os.path.splitext(os.path.basename(manifest_path))[0]
        print(f"Building skill: {skill_name}")
        write_skill(manifest_path, snippets_dirs, args.claude_skills_dir, args.attributes, args.custom_file)
        write_skill(manifest_path, snippets_dirs, args.agents_skills_dir, args.attributes, args.custom_file)

    scope_info = f" (scopes: {', '.join(args.scopes)})" if args.scopes else ""
    print(f"Built {len(manifests)} skills{scope_info}.")


if __name__ == "__main__":
    main()
