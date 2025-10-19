from django import template

register = template.Library()

@register.filter
def soft_email(value: str) -> str:
    if not value:
        return ""
    # inserta espacios invisibles tras '@' y '.'
    return (
        value
        .replace("@", "&#8203;@")
        .replace(".", "&#8203;.")
    )
