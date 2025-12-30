from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import template

from website.fx import convert_amount


register = template.Library()


@register.filter(name='fx')
def fx(amount: object, to_currency: str) -> str:
    """Convert an AED amount to the selected currency and format with 2 decimals."""

    if amount is None or to_currency is None:
        return ''

    try:
        dec = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError):
        return str(amount)

    converted = convert_amount(dec, to_currency=to_currency, from_currency='AED')
    converted = converted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return f"{converted}"
