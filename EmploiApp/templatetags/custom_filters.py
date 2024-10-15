from django import template

register = template.Library()

@register.filter
def filter_by_classroom_and_day(seances, classroom, day):
    return seances.filter(classroom=classroom, day_week=day)
