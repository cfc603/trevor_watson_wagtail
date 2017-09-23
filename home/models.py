from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey


# Pages
class AboutPage(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle", classname="full"),
        FieldPanel("body", classname="full")
    ]

    search_fields = Page.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("body")
    ]


class HomePage(Page):
    subtitle = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]


# Snippets
@register_snippet
class SocialLink(models.Model):
    FACEBOOK = "FB"
    GITHUB = "GH"
    GOOGLEPLUS = "GP"
    INSTAGRAM = "IG"
    LINKEDIN = "LI"
    PINTEREST = "PT"
    TWITTER = "TW"
    YOUTUBE = "YT"

    SOCIAL_CHOICES = (
        (FACEBOOK, "Facebook"),
        (GOOGLEPLUS, "Google+"),
        (GITHUB, "GitHub"),
        (INSTAGRAM, "Instagram"),
        (LINKEDIN, "LinkedIn"),
        (PINTEREST, "Pinterest"),
        (TWITTER, "Twitter"),
        (YOUTUBE, "YouTube"),
    )

    SOCIAL_ICONS = {
        FACEBOOK:"fa-facebook",
        GOOGLEPLUS:"fa-google-plus",
        GITHUB:"fa-github",
        INSTAGRAM:"fa-instagram",
        LINKEDIN:"fa-linkedin",
        PINTEREST:"fa-pinterest",
        TWITTER:"fa-twitter",
        YOUTUBE:"fa-youtube-play",
    }

    link = models.URLField()
    site = models.CharField(max_length=2, choices=SOCIAL_CHOICES)

    panels = [
        FieldPanel("link", classname="full"),
        FieldPanel("site"),
    ]

    def __unicode__(self):
        return "{}".format(self.get_site_display())

    def get_social_icon(self):
        return self.SOCIAL_ICONS[self.site]
