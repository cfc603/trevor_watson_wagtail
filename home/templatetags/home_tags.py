from django import template

from home.models import SocialLink

register = template.Library()


@register.inclusion_tag("home/tags/social_links.html")
def social_links(icons=False):
    return {
        "icons": icons,
        "social_links": SocialLink.objects.order_by("site")
    }