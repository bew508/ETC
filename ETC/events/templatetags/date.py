from datetime import datetime
from django import template

import re

register = template.Library()

@register.filter
def date(date):
    # Convert date, raise an error on issue
    print(date)
    try:
        return datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%y')
    except:
        raise template.TemplateSyntaxError('Invalid date format')