from django import template

register = template.Library()

@register.filter(name='currency')
def currency(value):
    """
    Formats a Decimal/float as 'R$ 1.234,56'.
    """
    if value is None:
        return ''
    try:
        # Format with comma as thousands separator and dot as decimal separator
        formatted = '{:,.2f}'.format(float(value))
        # Swap separators to Brazilian standard: R$ 1,234.56 -> R$ 1.234,56
        main_part, decimal_part = formatted.split('.')
        main_part = main_part.replace(',', '.')
        return f'R$ {main_part},{decimal_part}'
    except (ValueError, TypeError):
        return value
