from django import template

register = template.Library()


@register.simple_tag
def mediapath(image_name):
    if image_name:
        return f"/media/{image_name}"
    else:
        return ""