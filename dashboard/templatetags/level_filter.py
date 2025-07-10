from django import template

register = template.Library()

@register.filter(name='get_level')
def get_level(score):
    if score >= 6:
        return 'High'
    elif score >= 4:
        return 'Moderate'
    elif score == 0 or score == 1:
        return 'Very Low'
    else:
        return 'Low'
