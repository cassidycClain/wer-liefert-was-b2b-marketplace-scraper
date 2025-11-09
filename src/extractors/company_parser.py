from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .utils import get_logger, normalize_whitespace

logger = get_logger(__name__)

@dataclass
class CompanyContact:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

@dataclass
class CompanyAddress:
    street: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country_code: Optional[str] = None
    full: Optional[str] = None

@dataclass
class CompanySummary:
    company_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    homepage: Optional[str] = None
    address: Optional[CompanyAddress] = None
    employee_count: Optional[str] = None
    founding_year: Optional[int] = None
    description: Optional[str] = None
    region: Optional[str] = None
    logo_url: Optional[str] = None
    details_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        if self.address:
            result["address"] = asdict(self.address)
        return result

def _extract_text(element) -> str:
    return normalize_whitespace(element.get_text(strip=True)) if element else ""

def parse_company_list(html: str, base_url: str) -> List[Dict[str, Any]]:
    """
    Parse the WLW search results page for company summaries.
    The exact CSS selectors are best-effort and may need tweaks if WLW changes their layout.
    """
    soup = BeautifulSoup(html, "html.parser")
    # This class is hypothetical; adjust if integrating with real HTML.
    cards = soup.select("[data-test='company-result-card'], article.company-item, div.company-card")

    companies: List[Dict[str, Any]] = []
    logger.info("Found %s potential company cards in search results.", len(cards))

    for card in cards:
        name_el = (
            card.select_one("[data-test='company-name']")
            or card.select_one("h2")
            or card.select_one("h3")
        )
        name = _extract_text(name_el)

        # Attempt to extract ID from data attributes or link
        company_id = card.get("data-id") or card.get("data-company-id")
        details_link = (
            card.select_one("a[data-test='company-link']")
            or card.select_one("a[href*='/firmen/']")
            or card.find("a")
        )
        details_url = None
        if details_link and details_link.has_attr("href"):
            details_url = urljoin(base_url, details_link["href"])
            if not company_id:
                company_id = details_link.get("data-id") or details_link["href"].strip("/").split("-")[-1]

        email_el = card.select_one("a[href^='mailto:']")
        email = ""
        if email_el and email_el.has_attr("href"):
            email = email_el["href"].replace("mailto:", "").strip()

        phone_el = card.select_one("a[href^='tel:']")
        phone_number = ""
        if phone_el and phone_el.has_attr("href"):
            phone_number = phone_el["href"].replace("tel:", "").strip()

        homepage_el = card.select_one("a[href^='http']")
        homepage = ""
        if homepage_el and homepage_el.has_attr("href"):
            homepage = homepage_el["href"].strip()

        address_el = (
            card.select_one("[data-test='company-address']")
            or card.select_one(".address")
        )
        address_full = _extract_text(address_el)
        address = CompanyAddress(full=address_full)

        employee_el = card.find(string=lambda s: s and "Mitarbeiter" in s)
        employee_count = normalize_whitespace(employee_el) if employee_el else None

        description_el = (
            card.select_one("[data-test='company-description']")
            or card.select_one(".description")
        )
        description = _extract_text(description_el)

        logo_el = card.select_one("img")
        logo_url = logo_el["src"] if logo_el and logo_el.has_attr("src") else None

        summary = CompanySummary(
            company_id=company_id,
            name=name or None,
            email=email or None,
            phone_number=phone_number or None,
            homepage=homepage or None,
            address=address,
            employee_count=employee_count,
            founding_year=None,  # often only available on details page
            description=description or None,
            region=None,
            logo_url=logo_url,
            details_url=details_url,
        )
        companies.append(summary.to_dict())

    return companies

def parse_company_details(html: str, company_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse a single company's detail page for richer information like contact persons,
    certificates and a more structured address.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Name and description
    name_el = (
        soup.select_one("[data-test='company-name']")
        or soup.select_one("h1")
        or soup.select_one("h2")
    )
    name = _extract_text(name_el)

    description_el = (
        soup.select_one("[data-test='company-description']")
        or soup.select_one("section.description")
        or soup.select_one("p.lead")
    )
    description = _extract_text(description_el)

    # Contact email, phone, homepage
    email_el = soup.select_one("a[href^='mailto:']")
    email = ""
    if email_el and email_el.has_attr("href"):
        email = email_el["href"].replace("mailto:", "").strip()

    phone_el = soup.select_one("a[href^='tel:']")
    phone_number = ""
    if phone_el and phone_el.has_attr("href"):
        phone_number = phone_el["href"].replace("tel:", "").strip()

    homepage_el = soup.select_one("a[href^='http']")
    homepage = ""
    if homepage_el and homepage_el.has_attr("href"):
        homepage = homepage_el["href"].strip()

    # Address breakdown best effort
    address_container = (
        soup.select_one("[data-test='company-address']")
        or soup.select_one("address")
        or soup.select_one(".address")
    )
    address_full = _extract_text(address_container)
    street = None
    postal_code = None
    city = None
    country_code = None

    # Very simple heuristics
    if address_full:
        parts = [p.strip() for p in address_full.split(",") if p.strip()]
        if parts:
            street = parts[0]
        if len(parts) >= 2:
            # Try to extract postal code and city from second part
            tokens = parts[1].split()
            if tokens:
                postal_code = tokens[0]
                city = " ".join(tokens[1:]) or None
        if len(parts) >= 3:
            country_code = parts[-1].split()[-1].upper()

    address = CompanyAddress(
        street=street,
        postal_code=postal_code,
        city=city,
        country_code=country_code,
        full=address_full or None,
    )

    # Employee count and founding year
    employee_count = None
    founding_year = None

    facts_section = soup.find(string=lambda s: s and ("Gründungsjahr" in s or "Mitarbeiteranzahl" in s))
    if facts_section:
        # Walk up a bit to parse nearby key-value pairs
        parent = facts_section.parent
        text_block = normalize_whitespace(parent.get_text(" "))
        if "Gründungsjahr" in text_block:
            try:
                for token in text_block.split():
                    if token.isdigit() and len(token) == 4:
                        founding_year = int(token)
                        break
            except ValueError:
                founding_year = None
        if "Mitarbeiter" in text_block:
            # Assign full phrase
            start = text_block.find("Mitarbeiter")
            employee_count = text_block[start:].strip()

    # Contacts
    contacts: List[CompanyContact] = []
    contact_blocks = soup.select("[data-test='contact-person'], .contact-person")
    for block in contact_blocks:
        name_el = block.select_one("h3, h4, .name")
        role_el = block.select_one(".role, .position")
        mail_el = block.select_one("a[href^='mailto:']")

        full_name = _extract_text(name_el)
        first_name = None
        last_name = None
        if full_name:
            tokens = full_name.split()
            if len(tokens) >= 2:
                first_name = tokens[0]
                last_name = " ".join(tokens[1:])
            else:
                first_name = full_name

        email_contact = None
        if mail_el and mail_el.has_attr("href"):
            email_contact = mail_el["href"].replace("mailto:", "").strip()

        contact = CompanyContact(
            first_name=first_name,
            last_name=last_name,
            email=email_contact,
            role=_extract_text(role_el) or None,
        )
        contacts.append(contact)

    # Certificates (best effort)
    certificates: List[str] = []
    cert_section = soup.find(string=lambda s: s and "Zertifizierungen" in s)
    if cert_section:
        container = cert_section.parent
        items = container.find_all("li")
        for item in items:
            text = _extract_text(item)
            if text:
                certificates.append(text)

    # Products (best effort)
    products: List[str] = []
    product_items = soup.select("[data-test='product-name'], .product-list li, section.products li")
    for item in product_items:
        text = _extract_text(item)
        if text:
            products.append(text)

    details = {
        "company_id": company_id,
        "name": name or None,
        "email": email or None,
        "phone_number": phone_number or None,
        "homepage": homepage or None,
        "address": {
            "street": address.street,
            "postal_code": address.postal_code,
            "city": address.city,
            "country_code": address.country_code,
            "full": address.full,
        },
        "employee_count": employee_count,
        "founding_year": founding_year,
        "description": description or None,
        "products": products,
        "contacts": [asdict(c) for c in contacts],
        "certificates": certificates,
    }

    return details