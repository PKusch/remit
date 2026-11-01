"""check_staleness.py: old legal content must fail the build, and bad input must be a usage error."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = str(ROOT / "scripts" / "check_staleness.py")


def run(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


class Staleness(unittest.TestCase):
    def test_a_generous_limit_passes(self):
        r = run("--max-age-days", "100000", "--today", "2026-11-02")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0 stale", r.stdout)

    def test_years_later_every_file_is_stale_and_the_build_fails(self):
        r = run("--today", "2035-01-01")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Do not just bump it", r.stdout)

    def test_a_zero_day_limit_flags_anything_not_verified_today(self):
        r = run("--max-age-days", "0", "--today", "2035-01-01")
        self.assertEqual(r.returncode, 1)

    def test_a_negative_limit_is_refused_at_the_argument(self):
        r = run("--max-age-days", "-1")
        self.assertEqual(r.returncode, 2)
        self.assertIn("cannot be negative", r.stderr)

    def test_a_mistyped_date_is_a_usage_error_not_a_traceback(self):
        r = run("--today", "next tuesday")
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)


if __name__ == "__main__":
    unittest.main()
