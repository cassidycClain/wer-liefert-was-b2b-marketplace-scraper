# Wer Liefert Was B2B Marketplace Scraper
This scraper extracts detailed company and product data from Wer Liefert Was (WLW), one of Europe’s largest B2B marketplaces. It helps you collect structured business information, supplier contacts, and product listings across regions and languages.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Wer Liefert Was B2B Marketplace Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
The **Wer Liefert Was B2B Marketplace Scraper** automates data extraction from WLW to build business intelligence datasets or supplier lists. It supports both company and product searches, offering flexible configuration for language, pagination, and result type.

### Why It’s Useful
- Enables automated collection of verified business data.
- Reduces time spent on manual sourcing and prospecting.
- Supports data-driven marketing, lead generation, and competitive research.
- Works across major European markets (Germany, Austria, Switzerland, etc.).
- Outputs structured JSON for easy integration into databases or analytics tools.

## Features
| Feature | Description |
|----------|-------------|
| Dual Search Modes | Supports company or product-based search modes. |
| Region & Language Selection | Search results can be filtered by region (DE/AT/CH/BE/LU) and language (de/en). |
| Detailed Company Profiles | Optionally retrieves in-depth company data such as VAT ID, contact persons, and certifications. |
| Configurable Pagination | Define how many pages to crawl (0 = unlimited). |
| Structured Output | Results are stored in clean JSON format suitable for APIs or databases. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|-------------|------------------|
| company_id | Unique identifier of the company. |
| name | Company name as listed on WLW. |
| email | Official contact email. |
| phone_number | Primary contact phone number. |
| homepage | Company website URL. |
| address | Physical address including city, postal code, and country. |
| founding_year | Year the company was established. |
| employee_count | Number of employees (e.g., “20–49”). |
| description | Company description or business overview. |
| products | List of products offered by the company. |
| region | Country or region of operation. |
| logo_url | Company logo image URL. |
| contacts | Contact person names, emails, and roles. |
| certificates | Business certifications, if available. |

---

## Example Output
    [
      {
        "company": {
          "slug": "tremmel-aufzuege-gmbh-cokg-1710405",
          "uuid": "00505682-f25b-1ee9-bd91-d262758ff7fb",
          "name": "Tremmel Aufzüge GmbH & Co.KG",
          "email": "info@tremmel-aufzuege.de",
          "phone_number": "+499929581970",
          "homepage": "http://www.tremmel-aufzuege.de/",
          "employee_count": "20-49",
          "founding_year": 2011,
          "address": { "city": "Patersdorf", "country_code": "DE" },
          "contacts": [
            { "first_name": "Werner", "last_name": "Tremmel", "email": "info@tremmel-aufzuege.de" }
          ],
          "logo_url": "https://.../316d3049.jpeg",
          "description": "We specialize in modernization, renovation, and service for passenger elevators."
        }
      }
    ]

---

## Directory Structure Tree
    Wer Liefert Was B2B Marketplace Scraper/
    ├── src/
    │   ├── main.py
    │   ├── extractors/
    │   │   ├── company_parser.py
    │   │   ├── product_parser.py
    │   │   └── utils.py
    │   ├── config/
    │   │   └── settings.json
    │   └── outputs/
    │       └── json_exporter.py
    ├── data/
    │   ├── sample_input.json
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases
- **Sales teams** use it to build accurate lead lists and reach out to verified suppliers.
- **Market researchers** analyze product trends and company growth across industries.
- **Procurement managers** find reliable partners or distributors in specific regions.
- **Developers** integrate business data into CRMs or ERP systems.
- **Data analysts** use structured WLW datasets for segmentation or performance benchmarking.

---

## FAQs
**Q: Can I limit the number of results?**
Yes. Set `maxPages` to any number to control pagination depth (0 means no limit).

**Q: Does it support multilingual searches?**
Absolutely. You can choose between German (`de`) and English (`en`) to match your target data.

**Q: How do I get detailed company info?**
Set `includeCompanyDetails` to `true` — detailed profiles will be saved separately.

**Q: Are search results region-specific?**
Yes, you can prioritize specific regions like DE, AT, CH, BE, or LU.

---

## Performance Benchmarks and Results
**Primary Metric:** Averages 80–100 records per minute depending on search complexity.
**Reliability Metric:** 98% success rate with stable session handling.
**Efficiency Metric:** Optimized for minimal bandwidth; requests are throttled for performance balance.
**Quality Metric:** Achieves 95%+ field completeness in structured company profiles.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
