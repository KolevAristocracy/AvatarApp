from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='get_question_field')
def get_question_field(form, question_pk):
    """
    A custom template filter to retrieve a specific field from a form
    by constructing its name from a questions primary key
    """

    field_name = f'question_{question_pk}'
    try:
        return form[field_name]
    except KeyError:
        return None