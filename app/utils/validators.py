# app/utils/validators.py
import re
import validators

def is_valid_upi(upi_id: str) -> bool:
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+$', upi_id))

def is_valid_url(url: str) -> bool:
    return validators.url(url)

def is_valid_phone(phone: str) -> bool:
    # Basic Indian phone validation
    return bool(re.match(r'^(\+91[\s-]?)?[6-9]\d{9}$', phone))
