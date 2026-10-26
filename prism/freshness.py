"""Measure ingestion tails without interpreting partial months as a trend."""
from datetime import date
import statistics
import threading
import time

from . import cache, ch

_LOCK = threading.Lock()
TTL = 21600


def news() -> dict:
    today = date.today()
    key = cache.key('freshness.news', today.isoformat(), ch.NEWS_LAST_MONTH)
    with _LOCK:
        hit = cache.get(key)
        if hit:
            return {**hit, 'age_seconds': round(time.time() - hit['checked_at'])}
        try:
            rows = ch.chq_rows(
                'SELECT toString(toStartOfMonth(datetime)), count() FROM '
                f"{ch.TABLE['news']} WHERE datetime >= addMonths(toDate('{today:%Y-%m}-01'), -12) "
                f"AND datetime < toDate('{today:%Y-%m}-01') GROUP BY 1 ORDER BY 1", timeout=30)
            months = {m: int(n) for m, n in rows}
            baseline = [n for m, n in months.items() if m < ch.NEWS_LAST_MONTH][-6:]
            median = statistics.median(baseline) if baseline else None
            tail = [{'month': m, 'articles': n,
                     'fraction_of_baseline': round(n / median, 3) if median else None}
                    for m, n in months.items() if m >= ch.NEWS_LAST_MONTH]
            out = {'available': True, 'checked_at': time.time(), 'age_seconds': 0,
                   'refresh_seconds': TTL, 'default_until': ch.NEWS_LAST_MONTH,
                   'last_observed_complete_calendar_month': max(months) if months else None,
                   'baseline_monthly_articles': median, 'tail': tail,
                   'cutoff_review_needed': bool(tail and median and
                                               any(x['articles'] >= median * .5 for x in tail)),
                   'note': 'Measured ingest volumes. A calendar month being over does not '
                           'prove its ingestion is complete. The report cutoff remains an explicit policy.'}
            cache.put(key, out, TTL)
            return out
        except Exception as e:
            return {'available': False, 'default_until': ch.NEWS_LAST_MONTH,
                    'checked_at': time.time(), 'reason': str(e),
                    'note': 'Freshness measurement unavailable; retaining the explicit report cutoff.'}
