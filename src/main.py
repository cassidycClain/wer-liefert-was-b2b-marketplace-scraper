import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from extractors.company_parser import (
    parse_company_list,
    parse_company_details,
)
from extractors.product_parser import parse_product_list
from extractors.utils import (
    build_search_url,
    fetch_page,
    get_logger,
    load_json_file,
)
from outputs.json_exporter import export_to_json

logger = get_logger(__name__)

def load_settings(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        logger.warning("Settings file %s not found, using built-in defaults.", config_path)
        return {
            "base_url": "https://www.wlw.de",
            "language": "de",
            "region": "DE",
            "mode": "company",
            "max_pages": 1,
            "include_company_details": True,
            "output_dir": "data",
            "output_filename": "sample_output.json",
        }

    return load_json_file(config_path)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Wer Liefert Was B2B Marketplace Scraper"
    )
    parser.add_argument(
        "--query",
        "-q",
        required=False,
        help="Search query (e.g. 'Aufzüge', 'Metallbau'). "
             "If not provided, will try to read from data/sample_input.json.",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["company", "product"],
        help="Search mode: 'company' or 'product'.",
    )
    parser.add_argument(
        "--region",
        "-r",
        help="Region code such as DE, AT, CH, BE, LU.",
    )
    parser.add_argument(
        "--language",
        "-l",
        help="Language code such as 'de' or 'en'.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to crawl (0 means unlimited).",
    )
    parser.add_argument(
        "--no-details",
        action="store_true",
        help="Skip detailed company profile extraction.",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=str(Path(__file__).parent / "config" / "settings.json"),
        help="Path to JSON settings file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Override output JSON file path.",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default=str(Path(__file__).parents[1] / "data" / "sample_input.json"),
        help="Optional JSON file with default query and options.",
    )
    return parser.parse_args()

def resolve_effective_config(
    base_settings: Dict[str, Any], args: argparse.Namespace
) -> Dict[str, Any]:
    """
    Merge settings.json, sample_input.json (optional) and CLI args
    into one effective configuration dictionary.
    CLI arguments have the highest precedence.
    """
    effective = dict(base_settings)

    # Load optional input file with query preset(s)
    input_path = Path(args.input)
    if input_path.exists():
        try:
            input_data = load_json_file(input_path)
            if isinstance(input_data, dict):
                effective.update(input_data)
                logger.info("Loaded additional defaults from %s", input_path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to read %s: %s", input_path, exc)

    # CLI overrides
    if args.mode:
        effective["mode"] = args.mode
    if args.region:
        effective["region"] = args.region
    if args.language:
        effective["language"] = args.language
    if args.max_pages is not None:
        effective["max_pages"] = args.max_pages
    if args.no_details:
        effective["include_company_details"] = False
    if args.output:
        effective["output_filename"] = args.output

    # Query can come from CLI or input JSON
    query = args.query or effective.get("query")
    if not query:
        logger.error(
            "No search query provided. Use --query or set 'query' in sample_input.json."
        )
        sys.exit(1)

    effective["query"] = query
    return effective

def scrape_company_mode(
    base_url: str,
    query: str,
    region: str,
    language: str,
    max_pages: int,
    include_details: bool,
) -> List[Dict[str, Any]]:
    session = fetch_page.create_session()
    page = 1
    all_companies: List[Dict[str, Any]] = []

    while True:
        search_url = build_search_url(
            base_url=base_url,
            query=query,
            mode="company",
            region=region,
            language=language,
            page=page,
        )
        logger.info("Fetching company search results page %s: %s", page, search_url)

        html_text = fetch_page(session, search_url)
        if not html_text:
            logger.info("Empty response for page %s, stopping.", page)
            break

        companies_on_page = parse_company_list(html_text, base_url=base_url)
        if not companies_on_page:
            logger.info("No more companies found on page %s, stopping.", page)
            break

        if include_details:
            for company in companies_on_page:
                details_url = company.get("details_url")
                if not details_url:
                    continue
                logger.info("Fetching company details: %s", details_url)
                details_html = fetch_page(session, details_url)
                if not details_html:
                    logger.warning("No details HTML for %s", details_url)
                    continue
                details_data = parse_company_details(details_html, company_id=company.get("company_id"))
                company["details"] = details_data

        all_companies.extend(companies_on_page)
        logger.info("Accumulated %s company records so far.", len(all_companies))

        if max_pages and max_pages > 0 and page >= max_pages:
            break

        page += 1

    return all_companies

def scrape_product_mode(
    base_url: str,
    query: str,
    region: str,
    language: str,
    max_pages: int,
) -> List[Dict[str, Any]]:
    session = fetch_page.create_session()
    page = 1
    all_products: List[Dict[str, Any]] = []

    while True:
        search_url = build_search_url(
            base_url=base_url,
            query=query,
            mode="product",
            region=region,
            language=language,
            page=page,
        )
        logger.info("Fetching product search results page %s: %s", page, search_url)

        html_text = fetch_page(session, search_url)
        if not html_text:
            logger.info("Empty response for page %s, stopping.", page)
            break

        products_on_page = parse_product_list(html_text, base_url=base_url)
        if not products_on_page:
            logger.info("No more products found on page %s, stopping.", page)
            break

        all_products.extend(products_on_page)
        logger.info("Accumulated %s product records so far.", len(all_products))

        if max_pages and max_pages > 0 and page >= max_pages:
            break

        page += 1

    return all_products

def main() -> None:
    args = parse_args()
    settings_path = Path(args.config)
    base_settings = load_settings(settings_path)
    config = resolve_effective_config(base_settings, args)

    base_url: str = config.get("base_url", "https://www.wlw.de")
    query: str = config["query"]
    region: str = config.get("region", "DE")
    language: str = config.get("language", "de")
    mode: str = config.get("mode", "company")
    max_pages: int = int(config.get("max_pages", 1) or 0)
    include_details: bool = bool(config.get("include_company_details", True))

    output_dir = Path(config.get("output_dir", "data"))
    output_filename = config.get("output_filename", "sample_output.json")
    output_path = Path(output_filename)
    if not output_path.is_absolute():
        output_path = output_dir / output_filename

    logger.info(
        "Starting WLW scraper | mode=%s | query=%s | region=%s | language=%s | max_pages=%s",
        mode,
        query,
        region,
        language,
        max_pages or "unlimited",
    )

    if mode == "company":
        results = scrape_company_mode(
            base_url=base_url,
            query=query,
            region=region,
            language=language,
            max_pages=max_pages,
            include_details=include_details,
        )
    else:
        results = scrape_product_mode(
            base_url=base_url,
            query=query,
            region=region,
            language=language,
            max_pages=max_pages,
        )

    logger.info("Scraping completed. Total records: %s", len(results))

    export_to_json(results, output_path)
    logger.info("Results exported to %s", output_path.resolve())

if __name__ == "__main__":
    main()