#!/usr/bin/env python3
"""Regression tests for the --scope / --platforms filtering in build-skills.py.

Run: python3 scripts/test_build_skills.py

Guards against two bugs found in practice:
  1. A platform qualifier used in a manifest name (e.g. "factory") missing
     from the --platforms default list, so it slips through the scope
     filter unrecognised and gets built regardless of --scope.
  2. Substring matching mistaking a shorter qualifier for a longer compound
     one that contains it (e.g. "mediawiki" matching inside the unrelated
     "docker-mediawiki" qualifier), leaking skills across scopes.
"""

import glob
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

import importlib.util
spec = importlib.util.spec_from_file_location(
    "build_skills", os.path.join(os.path.dirname(__file__), "build-skills.py")
)
build_skills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_skills)

platform_qualifier = build_skills.platform_qualifier

DEFAULT_PLATFORMS = [
    p.strip() for p in
    "mediawiki,nodejs,ansible,docker-mediawiki,factory".split(",")
    if p.strip()
]

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GESINN_DEV_ROOT = os.environ.get(
    "GESINN_DEV_ROOT",
    os.path.normpath(os.path.join(REPO_ROOT, "..", "..", "..")),  # .../github.com/gesinn-it-pub/<repo> -> .../
)
DOCSM_MANIFESTS_DIR = os.path.join(
    GESINN_DEV_ROOT, "github.com", "gesinn-it", "gesinn-it-docs-master", "skills", "manifests"
)


def manifest_names(manifests_dir):
    return sorted(
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(os.path.join(manifests_dir, "*.yml"))
    )


class TestPlatformQualifier(unittest.TestCase):

    def test_compound_qualifier_not_confused_with_contained_shorter_one(self):
        # Regression: "mediawiki" is a substring of "docker-mediawiki" — the
        # qualifier must resolve to the full compound, not the short one.
        self.assertEqual(
            platform_qualifier("commit-do-docker-mediawiki", DEFAULT_PLATFORMS),
            "docker-mediawiki",
        )
        self.assertEqual(
            platform_qualifier("debug-fix-docker-mediawiki", DEFAULT_PLATFORMS),
            "docker-mediawiki",
        )

    def test_plain_mediawiki_qualifier_still_resolves(self):
        self.assertEqual(
            platform_qualifier("test-write-php-mediawiki", DEFAULT_PLATFORMS),
            "mediawiki",
        )

    def test_factory_qualifier_recognised(self):
        # Regression: "factory" was missing from the --platforms default,
        # so factory skills were treated as scope-less and always built.
        self.assertEqual(
            platform_qualifier("code-write-python-factory", DEFAULT_PLATFORMS),
            "factory",
        )

    def test_universal_skill_has_no_qualifier(self):
        for name in ("commit-do", "doc-write", "release-do"):
            self.assertIsNone(platform_qualifier(name, DEFAULT_PLATFORMS))

    def test_unknown_platform_returns_none(self):
        self.assertIsNone(
            platform_qualifier("code-write-rust-embedded", DEFAULT_PLATFORMS)
        )

    def test_docker_mediawiki_scope_excludes_plain_mediawiki_skills(self):
        # This is exactly the filter build-skills.py applies for --scope.
        scopes = {"docker-mediawiki"}
        names = [
            "commit-do-docker-mediawiki",
            "test-write-php-mediawiki",
            "code-write-python-factory",
            "commit-do",
        ]
        matched = [
            n for n in names
            if (q := platform_qualifier(n, DEFAULT_PLATFORMS)) is None or q in scopes
        ]
        self.assertEqual(matched, ["commit-do-docker-mediawiki", "commit-do"])

    def test_mediawiki_scope_excludes_docker_mediawiki_and_factory_skills(self):
        scopes = {"mediawiki"}
        names = [
            "commit-do-docker-mediawiki",
            "test-write-php-mediawiki",
            "code-write-python-factory",
            "commit-do",
        ]
        matched = [
            n for n in names
            if (q := platform_qualifier(n, DEFAULT_PLATFORMS)) is None or q in scopes
        ]
        self.assertEqual(matched, ["test-write-php-mediawiki", "commit-do"])


class TestPlatformsListCoversRealManifests(unittest.TestCase):
    """Fails if a new platform qualifier is introduced in manifests without
    updating build-skills.py's --platforms default — the exact way the
    "factory" bug slipped in originally."""

    def _assert_all_named_platforms_are_known(self, manifests_dir):
        names = manifest_names(manifests_dir)
        if not names:
            self.skipTest(f"no manifests found under {manifests_dir}")

        unrecognised = []
        for name in names:
            # A manifest name with more than 2 hyphen segments beyond
            # domain-action is expected to end in a known platform qualifier.
            segments = name.split("-")
            if len(segments) <= 2:
                continue  # domain-action only, no qualifier expected
            if platform_qualifier(name, DEFAULT_PLATFORMS) is None:
                unrecognised.append(name)

        self.assertEqual(
            unrecognised, [],
            f"Manifest name(s) with an apparent platform/language suffix not "
            f"covered by build-skills.py's --platforms default: {unrecognised}. "
            f"Add the new qualifier to the --platforms default list."
        )

    def test_docsmp_manifests(self):
        manifests_dir = os.path.join(REPO_ROOT, "skills", "manifests")
        self._assert_all_named_platforms_are_known(manifests_dir)

    def test_docsm_manifests_if_present(self):
        if not os.path.isdir(DOCSM_MANIFESTS_DIR):
            self.skipTest(f"DOCSM not checked out at {DOCSM_MANIFESTS_DIR}")
        self._assert_all_named_platforms_are_known(DOCSM_MANIFESTS_DIR)


if __name__ == "__main__":
    unittest.main()
