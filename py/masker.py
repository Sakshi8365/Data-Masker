def mask_text(text: str, config: dict = None) -> tuple[str, dict]:
    from faker import Faker
    import re

    fake = Faker()
    summary = {
        "names": 0,
        "emails": 0,
        "phones": 0,
        "companies": 0,
        "locations": 0
    }

    if config is None:
        config = {key: True for key in summary}

    if config.get("emails", True):
        email_pattern = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
        found_emails = re.findall(email_pattern, text)
        text = re.sub(email_pattern, lambda m: fake.email(), text)
        summary["emails"] = len(found_emails)

    if config.get("phones", True):
        phone_pattern = r'\b\d{10}\b'
        found_phones = re.findall(phone_pattern, text)
        text = re.sub(phone_pattern, lambda m: str(fake.random_int(min=6000000000, max=9999999999)), text)
        summary["phones"] = len(found_phones)

    if config.get("names", True):
        name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
        found_names = re.findall(name_pattern, text)
        text = re.sub(name_pattern, lambda m: fake.name(), text)
        summary["names"] = len(found_names)

    if config.get("companies", True):
        company_pattern = r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)* (Inc|Corp|Technologies|Ltd|LLC|Systems|Group|Labs)?\b'
        found_companies = re.findall(company_pattern, text)
        text = re.sub(company_pattern, lambda m: fake.company(), text)
        summary["companies"] = len(found_companies)

    if config.get("locations", True):
        location_pattern = r'\b(?:Mumbai|Bangalore|Delhi|Chennai|Pune|Hyderabad)\b'
        found_locations = re.findall(location_pattern, text)
        text = re.sub(location_pattern, lambda m: fake.city(), text)
        summary["locations"] = len(found_locations)

    return text, summary
