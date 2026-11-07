"""Test suite for the Nurse Shift-Swap Pack.

Verifies structure, required content, license correctness, education-only
disclaimers, neutral placeholders, and that build.py produces a well-formed
print-ready packet.

Education only - not medical advice.
Copyright (c) 2026 Asdale Dynamics, LLC. MIT License.
"""

import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOCS = [
    "docs/shift-swap-request-text.md",
    "docs/shift-swap-request-email.md",
    "docs/unit-approval-checklist.md",
    "docs/coverage-math-one-pager.md",
    "docs/swap-confirmation-tracker.md",
    "docs/thank-you-coupons.md",
]

PRINT_PAGES = [
    "print/shift-swap-request-text.html",
    "print/shift-swap-request-email.html",
    "print/unit-approval-checklist.html",
    "print/coverage-math-one-pager.html",
    "print/swap-confirmation-tracker.html",
    "print/thank-you-coupons.html",
]

DISCLAIMER_MARK = "medical advice"
CREDIT = "Asdale Dynamics, LLC"
LICENSE_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"

DOC_REQUIRED = {
    "docs/shift-swap-request-text.md": ["4-Part Formula", "easy out", "[Name]"],
    "docs/shift-swap-request-email.md": ["Subject:", "reply-all", "manager"],
    "docs/unit-approval-checklist.md": ["in writing", "overtime", "Step 1"],
    "docs/coverage-math-one-pager.md": ["zero-sum", "staffing", "overtime"],
    "docs/swap-confirmation-tracker.md": ["in writing", "approval", "Reminder"],
    "docs/thank-you-coupons.md": ["Presented to", "Signed:", "no authority"],
}

# Invented hospital/facility names are banned; neutral [Placeholders] are not.
BANNED_NAME_PATTERNS = ["St. Mary", "St. Luke", "General Hospital", "Memorial Hospital"]


class StructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            "README.md",
            "LICENSE",
            "STATUS.md",
            "build.py",
            "styles.css",
            *DOCS,
            *PRINT_PAGES,
        ]
        missing = [name for name in required if not (ROOT / name).is_file()]
        self.assertEqual(missing, [], f"Missing files: {missing}")

    def test_license_line_is_exact(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(LICENSE_LINE, license_text)
        self.assertIn("MIT License", license_text)

    def test_readme_credits_asdale(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(CREDIT, readme)
        self.assertIn("medical advice", readme.lower())
        self.assertIn("free", readme.lower())

    def test_docs_disclaim_medical_advice(self):
        for name in DOCS:
            with self.subTest(doc=name):
                text = (ROOT / name).read_text(encoding="utf-8").lower()
                self.assertIn(DISCLAIMER_MARK, text)

    def test_docs_use_neutral_placeholders(self):
        text = "\n".join((ROOT / n).read_text(encoding="utf-8") for n in DOCS)
        for pattern in BANNED_NAME_PATTERNS:
            self.assertNotIn(pattern, text)
        self.assertIn("[Name]", text)
        self.assertIn("[Date]", text)

    def test_docs_contain_expected_core_content(self):
        for name, needles in DOC_REQUIRED.items():
            text = (ROOT / name).read_text(encoding="utf-8")
            for needle in needles:
                self.assertIn(needle, text, f"{name} missing {needle!r}")

    def test_docs_cross_reference_pack_members(self):
        text_srcs = {n: (ROOT / n).read_text(encoding="utf-8") for n in DOCS}
        self.assertIn("coverage-math-one-pager.md", text_srcs["docs/unit-approval-checklist.md"])
        self.assertIn("unit-approval-checklist.md", text_srcs["docs/shift-swap-request-text.md"])
        self.assertIn("swap-confirmation-tracker.md", text_srcs["docs/shift-swap-request-email.md"])
        self.assertIn("thank-you-coupons.md", text_srcs["docs/swap-confirmation-tracker.md"])

    def test_distinction_from_sibling_packs(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("free-nurse-week-appreciation-pack", readme)
        self.assertIn("night-shift-survival-guide", readme)
        self.assertIn("whole unit", readme)
        self.assertIn("endurance", readme)


class _Checker(HTMLParser):
    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack:
            self.errors.append(f"unexpected </{tag}>")
        elif self.stack[-1] != tag:
            self.errors.append(f"expected </{self.stack[-1]}> got </{tag}>")
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.stack.pop()
                self.stack.pop()
        else:
            self.stack.pop()


class HtmlSheetTests(unittest.TestCase):
    def test_each_page_parses_and_has_shared_css(self):
        for name in PRINT_PAGES:
            path = ROOT / name
            text = path.read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn("<!DOCTYPE html>", text)
                self.assertIn('href="styles.css"', text)
                self.assertIn(DISCLAIMER_MARK, text)
                self.assertIn("Asdale Dynamics, LLC", text)
                self.assertEqual(text.count('class="sheet'), 1)
                checker = _Checker()
                checker.feed(text)
                checker.close()
                self.assertEqual(checker.errors, [], f"{name}: {checker.errors}")
                # the concatenation packet contains this sheet later, so no
                # cross-page <html>/<body> drift issues here: each standalone
                # page must open and close exactly one of each.
                self.assertEqual(text.count("<html lang=\"en\">"), 1)
                self.assertEqual(text.count("</html>"), 1)
                self.assertEqual(text.count("<body>"), 1)
                self.assertEqual(text.count("</article>"), 1)


class BuildTests(unittest.TestCase):
    def test_build_packet_contains_all_sheets(self):
        result = subprocess.run(
            [sys.executable, "build.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        packet = ROOT / "_build" / "nurse-shift-swap-packet.html"
        self.assertTrue(packet.is_file(), "build.py must write the packet")
        text = packet.read_text(encoding="utf-8")
        self.assertEqual(text.count('class="sheet'), len(PRINT_PAGES) + 1)
        for marker in [
            "Kind Shift-Swap Request Scripts",
            "Unit-Approval Checklist",
            "Coverage Math",
            "Swap-Confirmation Tracker",
            "Thank-You Coupons",
            LICENSE_LINE and "&copy; 2026 Asdale Dynamics, LLC",
        ]:
            self.assertIn(marker, text)
        # stylesheet must be inlined so the packet is self-contained
        self.assertNotIn('href="styles.css"', text)
        self.assertIn("@page", text)


if __name__ == "__main__":
    unittest.main()
