from django import template

from home.models import SocialLink

register = template.Library()


# Assignment Tags
@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


# Inclusion Tags
@register.inclusion_tag("home/tags/navigation.html", takes_context=True)
def navigation(context, parent, calling_page=None):
    menuitems = context['request'].site.root_page.get_children().live().in_menu()
    for menuitem in menuitems:
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.path.startswith(menuitem.path)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag("home/tags/social_links.html")
def social_links(icons=False):
    return {
        "icons": icons,
        "social_links": SocialLink.objects.order_by("site")
    }
