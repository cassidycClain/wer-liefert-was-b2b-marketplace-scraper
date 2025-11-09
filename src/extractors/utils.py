import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode, urljoin

import requests

_LOGGER_INITIALIZED = False

def _init_logging() -> None:
    global _LOGGER_INITIALIZED
    if _LOGGER_INITIALIZED:
        return
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    _LOGGER_INITIALIZED = True

def get_logger(name: str) -> logging.Logger:
    _init_logging()
    return logging.getLogger(name)

logger = get_logger(__name__)

@dataclass
class RetryConfig:
    retries: int = 3
    backoff_factor: float = 0.5
    timeout: float = 20.0

def create_session() -> requests.Session:
    """
    Create a requests session with basic headers suitable for scraping.
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0 Safari/537.36"
            ),
            "Accept-Language": "de,en;q=0.8",
        }
    )
    return session

def fetch_page(
    session: requests.Session,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    retry_config: Optional[RetryConfig] = None,
) -> str:
    """
    Fetch a single HTML page with retries and basic error handling.
    """
    retry_config = retry_config or RetryConfig()
    attempt = 0
    last_exception: Optional[Exception] = None

    while attempt <= retry_config.retries:
        try:
            response = session.get(
                url,
                params=params,
                timeout=retry_config.timeout,
            )
            if response.status_code >= 400:
                logger.warning(
                    "Got status code %s for %s with params %s",
                    response.status_code,
                    url,
                    params,
                )
            response.raise_for_status()
            return response.text
        except (requests.RequestException, Exception) as exc:  # noqa: BLE001
            last_exception = exc
            logger.warning(
                "Request error (attempt %s/%s) for %s: %s",
                attempt + 1,
                retry_config.retries + 1,
                url,
                exc,
            )
            if attempt >= retry_config.retries:
                break
            delay = retry_config.backoff_factor * (2**attempt)
            time.sleep(delay)
            attempt += 1

    logger.error("Failed to fetch %s after %s attempts", url, retry_config.retries + 1)
    if last_exception:
        logger.debug("Last exception: %s", last_exception)
    return ""

# Allow main.py to call `fetch_page.create_session()`
fetch_page.create_session = create_session  # type: ignore[attr-defined]

def normalize_whitespace(text: str) -> str:
    """
    Collapse consecutive whitespace into single spaces and strip.
    """
    return " ".join(text.split()) if text else ""

def safe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def build_search_url(
    base_url: str,
    query: str,
    mode: str,
    region: str,
    language: str,
    page: int = 1,
) -> str:
    """
    Construct a WLW-like search URL.
    This may not exactly match WLW's internal routing but works as a generic structure.
    """
    mode_segment = "firmen" if mode == "company" else "produkte"
    lang_segment = "de" if language == "de" else "en"
    path = f"/{lang_segment}/{mode_segment}/"
    params = {
        "q": query,
        "page": page,
        "country": region,
    }
    full_url = urljoin(base_url, path)
    return f"{full_url}?{urlencode(params)}"

def load_json_file(path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)