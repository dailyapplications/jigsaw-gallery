"""Small stdlib HTTP helper with a descriptive User-Agent (museum APIs ask for one)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "JigsawGalleryTools/1.0 (+https://github.com/dailyapplications/jigsaw-gallery; dailyapplications@gmail.com)"


def get_bytes(url: str, retries: int = 4, timeout: int = 60) -> bytes:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError) as e:  # includes HTTPError
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code in (400, 401, 404):
                break
            time.sleep(4 * (attempt + 1))  # 403/429 from rate limiting: back off
    raise RuntimeError(f"GET {url} failed: {last}")


def get_json(url: str, params: dict | None = None) -> dict:
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    return json.loads(get_bytes(url))
