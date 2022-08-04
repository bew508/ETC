from datetime import datetime
from django import template

register = template.Library()

@register.filter
def date(date):
    # Convert date, raise an error on issue
    try:
        return datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%y')
    except:
        raise template.TemplateSyntaxError('Invalid date format')