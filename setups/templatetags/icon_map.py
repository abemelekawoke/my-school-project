from django import template

register = template.Library()

ICON_MAP = {
    "year": "fa-calendar",
    "month": "fa-calendar-alt",
    "term": "fa-clock",
    "grade": "fa-layer-group",
    "section": "fa-columns",
    "subject": "fa-book",
    "teacher": "fa-chalkboard-teacher",
}

@register.filter
def get_icon(model_name):
    return ICON_MAP.get(model_name.lower(), "fa-database")
