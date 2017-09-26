from django import template
from django.db.models import Count

from portfolio.models import ProjectPage

register = template.Library()


@register.inclusion_tag("portfolio/tags/tag_nav.html", takes_context=True)
def tag_nav(context, count=None):
    if count:
        tags = ProjectPage.tags.annotate(
            project_count=Count("portfolio_projecttag_items")
        ).order_by("-project_count", "name")[:count]
    else:
        tags = ProjectPage.tags.annotate(
            project_count=Count("portfolio_projecttag_items")
        ).order_by("-project_count", "name")

    return {
        "current_tag": context["request"].GET.get("tag"),
        "tags": tags,
        "request": context["request"],
    }