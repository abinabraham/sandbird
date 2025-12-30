from __future__ import annotations

import json
import urllib.request
from decimal import Decimal, InvalidOperation

from django.core.cache import cache


CACHE_KEY = 'fx_rates_v1'
CACHE_TTL_SECONDS = 6 * 60 * 60


def _fetch_rates(base_currency: str = 'AED') -> dict[str, Decimal]:
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    with urllib.request.urlopen(url, timeout=6) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    rates = data.get('rates') or {}
    parsed: dict[str, Decimal] = {}
    for k, v in rates.items():
        try:
            parsed[str(k).upper()] = Decimal(str(v))
        except (InvalidOperation, TypeError):
            continue

    parsed[base_currency.upper()] = Decimal('1')
    return parsed


def get_rates(base_currency: str = 'AED') -> dict[str, Decimal]:
    base_currency = (base_currency or 'AED').upper()
    cached = cache.get(CACHE_KEY)
    if isinstance(cached, dict) and cached.get('_base') == base_currency:
        rates = cached.get('rates')
        if isinstance(rates, dict) and rates:
            return rates

    try:
        rates = _fetch_rates(base_currency=base_currency)
    except Exception:
        if isinstance(cached, dict):
            rates = cached.get('rates')
            if isinstance(rates, dict) and rates:
                return rates
        return {base_currency: Decimal('1')}

    cache.set(CACHE_KEY, {'_base': base_currency, 'rates': rates}, CACHE_TTL_SECONDS)
    return rates


def convert_amount(amount: Decimal, to_currency: str, from_currency: str = 'AED') -> Decimal:
    to_currency = (to_currency or from_currency).upper()
    from_currency = (from_currency or 'AED').upper()

    if to_currency == from_currency:
        return amount

    rates = get_rates(base_currency=from_currency)
    rate = rates.get(to_currency)
    if not rate:
        return amount

    return (amount * rate)
