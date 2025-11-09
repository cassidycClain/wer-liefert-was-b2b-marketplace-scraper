from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .utils import get_logger, normalize_whitespace

logger = get_logger(__name__)

@dataclass
class ProductSummary:
    name: Optional[str] = None
    company_name: Optional[str] = None
    company_id: Optional[str] = None
    product_url: Optional[str] = None
    company_url: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def _extract_text(element) -> str:
    return normalize_whitespace(element.get_text(strip=True)) if element else ""

def parse_product_list(html: str, base_url: str) -> List[Dict[str, Any]]:
    """
    Parse WLW product search result pages into a list of product summaries.
    """
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("[data-test='product-result-card'], article.product-item, div.product-card")

    logger.info("Found %s potential product cards in search results.", len(cards))

    products: List[Dict[str, Any]] = []

    for card in cards:
        product_name_el = (
            card.select_one("[data-test='product-name']")
            or card.select_one("h2")
            or card.select_one("h3")
        )
        product_name = _extract_text(product_name_el)

        product_link_el = card.select_one("a[data-test='product-link'], a[href*='/produkte/']")
        product_url = None
        if product_link_el and product_link_el.has_attr("href"):
            product_url = urljoin(base_url, product_link_el["href"])

        company_name_el = (
            card.select_one("[data-test='company-name']")
            or card.select_one(".company-name")
        )
        company_name = _extract_text(company_name_el)

        company_link_el = (
            card.select_one("a[data-test='company-link']")
            or card.select_one("a[href*='/firmen/']")
        )
        company_url = None
        company_id = None
        if company_link_el and company_link_el.has_attr("href"):
            href = company_link_el["href"]
            company_url = urljoin(base_url, href)
            company_id = company_link_el.get("data-id") or href.strip("/").split("-")[-1]

        description_el = (
            card.select_one("[data-test='product-description']")
            or card.select_one(".description")
        )
        description = _extract_text(description_el)

        region_el = card.select_one("[data-test='company-region'], .region")
        region = _extract_text(region_el) or None

        product_summary = ProductSummary(
            name=product_name or None,
            company_name=company_name or None,
            company_id=company_id,
            product_url=product_url,
            company_url=company_url,
            region=region,
            description=description or None,
        )
        products.append(product_summary.to_dict())

    return products