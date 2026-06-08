#!/usr/bin/env python3
"""Build Claude Code and agent skills from YAML composition manifests.

For each manifest in <manifests-dir>/*.yml:
  1. Read the skill name, description, and references list.
  2. Convert each referenced AsciiDoc snippet to Markdown.
  3. Write numbered reference files to <claude-skills-dir>/{name}/references/.
  4. Write a SKILL.md with frontmatter and a body that loads the references.

Also mirrors output to <agents-skills-dir>/{name}/ for VS Code Copilot / other agents.

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
"""

import argparse
import os
import subprocess
import sys
import yaml


def adoc_to_markdown(adoc_path):
    """Convert an AsciiDoc file to Markdown via asciidoctor + pandoc."""
    try:
        reduced = subprocess.run(
            ["asciidoctor-reducer", adoc_path],
            capture_output=True, text=True, check=True
        ).stdout

        tmp_adoc = "/tmp/skill-snippet.adoc"
        tmp_xml = "/tmp/skill-snippet.xml"
        with open(tmp_adoc, "w") as f:
            f.write(reduced)

        subprocess.run(
            ["asciidoctor", "-b", "docbook5", "-o", tmp_xml, tmp_adoc],
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


def write_skill(manifest_path, snippets_dir, output_base_dir):
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
    for i, ref_path in enumerate(references, start=1):
        adoc_path = os.path.join(snippets_dir, ref_path)
        if not os.path.exists(adoc_path):
            print(f"  WARNING: snippet not found: {adoc_path}", file=sys.stderr)
            continue

        parts = ref_path.replace("\\", "/").split("/")
        scope = parts[0]
        name = os.path.splitext(parts[-1])[0]
        ref_filename = f"{i:02d}-{scope}-{name}.md"
        ref_filepath = os.path.join(refs_dir, ref_filename)

        print(f"  Converting {ref_path} -> references/{ref_filename}")
        md_content = adoc_to_markdown(adoc_path)
        with open(ref_filepath, "w") as f:
            f.write(md_content + "\n")

        ref_lines.append(f"- `references/{ref_filename}`")

    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    ref_section = "\n".join(ref_lines) if ref_lines else "_No references._"
    with open(skill_md_path, "w") as f:
        f.write(f"""---
name: {skill_name}
description: >
  {description}
---

Load the following reference files before starting work:

{ref_section}
""")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifests-dir", default="skills/manifests",
                        help="Directory containing *.yml skill manifests (default: skills/manifests)")
    parser.add_argument("--snippets-dir", default="snippets",
                        help="Directory containing AsciiDoc snippets (default: snippets)")
    parser.add_argument("--claude-skills-dir", default=".claude/skills",
                        help="Output directory for Claude Code skills (default: .claude/skills)")
    parser.add_argument("--agents-skills-dir", default=".agents/skills",
                        help="Output directory for agent skills (default: .agents/skills)")
    parser.add_argument("--scope", default=None,
                        help="Only build skills whose name contains this string (e.g. 'mediawiki')")
    args = parser.parse_args()

    if not os.path.isdir(args.manifests_dir):
        print(f"No manifests directory found at {args.manifests_dir} — skipping skill build.")
        return

    manifests = sorted(
        f for f in os.listdir(args.manifests_dir) if f.endswith(".yml")
    )

    if args.scope:
        manifests = [f for f in manifests if args.scope in f]

    if not manifests:
        print("No manifest files found" + (f" matching scope '{args.scope}'" if args.scope else "") + ".")
        return

    for manifest_file in manifests:
        manifest_path = os.path.join(args.manifests_dir, manifest_file)
        skill_name = os.path.splitext(manifest_file)[0]
        print(f"Building skill: {skill_name}")
        write_skill(manifest_path, args.snippets_dir, args.claude_skills_dir)
        write_skill(manifest_path, args.snippets_dir, args.agents_skills_dir)

    scope_info = f" (scope: {args.scope})" if args.scope else ""
    print(f"Built {len(manifests)} skills{scope_info}.")


if __name__ == "__main__":
    main()
