"""Date/year parameters must be validated at the boundary and never reach SQL.

Regression for the 2026-10-29 finding: since/until were interpolated into
ClickHouse WHERE clauses unvalidated. These tests run offline — they assert the
validator's behaviour and, crucially, that a malformed date raises before any
query is issued (a stubbed chq_rows fails the test if it is ever called)."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('PRISM_CACHE_DIR', tempfile.mkdtemp(prefix='prism-inj-'))

from prism import ch, envelope, news, deep  # noqa: E402

# Values that must never reach SQL. Each either breaks out of the quoted literal
# or is simply not a date.
PAYLOADS = [
    "2024-01-01'",
    "2024-01-01' OR 1=1 --",
    "2024-01-01'; DROP TABLE marketai --",
    "2024-01-01' UNION SELECT password FROM users --",
    "' OR '1'='1",
    "2024-01-01\\",
    "notadate",
    "2024-13-01",      # impossible month
    "2024-01-32",      # impossible day
]
VALID = ["2024-01-01", "2024-01", "2024-06-01 12:00:00", "2026-06-01"]


class SafeDateTests(unittest.TestCase):
    def test_valid_dates_canonicalise(self):
        for v in VALID:
            self.assertRegex(ch.safe_date(v, "since"), r"^\d{4}-\d{2}-\d{2}")
        self.assertEqual(ch.safe_date("2024-03", "since"), "2024-03-01")

    def test_blank_passes_through_as_none(self):
        self.assertIsNone(ch.safe_date(None, "since"))
        self.assertIsNone(ch.safe_date("", "since"))
        self.assertIsNone(ch.safe_date("   ", "since"))

    def test_every_payload_is_rejected(self):
        for p in PAYLOADS:
            with self.assertRaises(ch.BadRequest, msg=f"accepted: {p!r}"):
                ch.safe_date(p, "since")

    def test_safe_year(self):
        self.assertEqual(ch.safe_year(2015, "since_year"), 2015)
        self.assertEqual(ch.safe_year("2015", "since_year"), 2015)
        self.assertIsNone(ch.safe_year(None, "since_year"))
        for bad in ["2015 OR 1=1", "2015;--", 9999, 1000, "nope"]:
            with self.assertRaises(ch.BadRequest, msg=f"accepted: {bad!r}"):
                ch.safe_year(bad, "since_year")


class BoundaryTests(unittest.TestCase):
    """A bad date must raise BEFORE any query. The stub makes any ClickHouse
    read a hard failure, so these pass only if validation happens first."""

    def _no_sql(self):
        return patch.object(ch, 'chq_rows',
                            side_effect=AssertionError("SQL issued for a bad date"))

    def test_bounds_rejects_payloads_without_querying(self):
        with self._no_sql():
            for p in PAYLOADS:
                with self.assertRaises(ch.BadRequest):
                    news._bounds(p, None)
                with self.assertRaises(ch.BadRequest):
                    news._bounds(None, p)

    def test_bounds_default_and_valid_still_work(self):
        start, end = news._bounds(None, None)
        self.assertRegex(start, r"^\d{4}-\d{2}-\d{2}$")
        self.assertRegex(end, r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(news._bounds("2024-01-01", "2024-06-01"),
                         ("2024-01-01", "2024-06-01"))

    def test_timeline_rejects_payload(self):
        with self._no_sql():
            for p in PAYLOADS:
                with self.assertRaises(ch.BadRequest):
                    deep.timeline("tesla", until=p)


class GuardTests(unittest.TestCase):
    """End to end through the envelope the MCP/REST layer uses: a bad date is a
    clean bad_request with no traceback, and no query is attempted."""

    def test_guard_returns_bad_request_without_trace_or_query(self):
        with patch.object(ch, 'chq_rows',
                          side_effect=AssertionError("SQL issued")):
            out = envelope.guard("news.trends", news.trends,
                                 "tesla", "monthly", "2024-01-01' OR 1=1 --", None)
        self.assertFalse(out["ok"])
        self.assertEqual(out["error"]["kind"], "bad_request")
        self.assertNotIn("trace", out.get("meta") or {})

    def test_guard_default_attaches_no_trace_on_upstream_error(self):
        # An upstream failure (dead cluster) must also not leak a traceback
        # unless PRISM_DEBUG is set.
        with patch.object(envelope, 'DEBUG', False), \
             patch.object(ch, 'chq_rows', side_effect=ch.CHError("CH down")):
            out = envelope.guard("news.trends", news.trends,
                                 "tesla", "monthly", "2024-01-01", None)
        self.assertFalse(out["ok"])
        self.assertNotIn("trace", out.get("meta") or {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
