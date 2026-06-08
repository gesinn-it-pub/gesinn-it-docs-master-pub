#!/usr/bin/env python3
"""Build Claude Code and agent skills from YAML composition manifests.

For each manifest in skills/manifests/*.yml:
  1. Read the skill name, description, and references list.
  2. Convert each referenced AsciiDoc snippet to Markdown.
  3. Write numbered reference files to .claude/skills/{name}/references/.
  4. Write a SKILL.md with frontmatter and a body that loads the references.

Also mirrors output to .agents/skills/{name}/ for VS Code Copilot / other agents.
"""

import os
import re
import subprocess
import sys
import yaml

MANIFESTS_DIR = "skills/manifests"
SNIPPETS_DIR = "snippets"
CLAUDE_SKILLS_DIR = ".claude/skills"
AGENTS_SKILLS_DIR = ".agents/skills"


def adoc_to_markdown(adoc_path):
    """Convert an AsciiDoc file to Markdown via asciidoctor + pandoc."""
    try:
        # Flatten any includes with asciidoctor-reducer first
        reduced = subprocess.run(
            ["asciidoctor-reducer", adoc_path],
            capture_output=True, text=True, check=True
        ).stdout

        # Write to a temp file for asciidoctor
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
        # Fall back to raw AsciiDoc content
        with open(adoc_path) as f:
            return f.read().strip()


def write_skill(manifest_path, output_base_dir):
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    skill_name = manifest["skill"]
    description = manifest["description"].strip()
    references = manifest.get("references", [])

    skill_dir = os.path.join(output_base_dir, skill_name)
    refs_dir = os.path.join(skill_dir, "references")
    os.makedirs(refs_dir, exist_ok=True)

    # Build reference files
    ref_lines = []
    for i, ref_path in enumerate(references, start=1):
        adoc_path = os.path.join(SNIPPETS_DIR, ref_path)
        if not os.path.exists(adoc_path):
            print(f"  WARNING: snippet not found: {adoc_path}", file=sys.stderr)
            continue

        basename = os.path.splitext(os.path.basename(ref_path))[0]
        ref_filename = f"{i:02d}-{basename}.md"
        ref_filepath = os.path.join(refs_dir, ref_filename)

        print(f"  Converting {ref_path} -> references/{ref_filename}")
        md_content = adoc_to_markdown(adoc_path)
        with open(ref_filepath, "w") as f:
            f.write(md_content + "\n")

        ref_lines.append(f"- `references/{ref_filename}`")

    # Write SKILL.md
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
    if not os.path.isdir(MANIFESTS_DIR):
        print(f"No manifests directory found at {MANIFESTS_DIR} — skipping skill build.")
        return

    manifests = sorted(
        f for f in os.listdir(MANIFESTS_DIR) if f.endswith(".yml")
    )

    if not manifests:
        print("No manifest files found.")
        return

    for manifest_file in manifests:
        manifest_path = os.path.join(MANIFESTS_DIR, manifest_file)
        skill_name = os.path.splitext(manifest_file)[0]
        print(f"Building skill: {skill_name}")
        write_skill(manifest_path, CLAUDE_SKILLS_DIR)
        write_skill(manifest_path, AGENTS_SKILLS_DIR)

    print(f"Built {len(manifests)} skills.")


if __name__ == "__main__":
    main()
