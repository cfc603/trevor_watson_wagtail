from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey


# Struct & Static Blocks
class HorizontalRuleStaticBlock(blocks.StaticBlock):

    class Meta:
        admin_text = "Display a horizontal rule."
        icon = "horizontalrule"
        template = "home/blocks/horizontal_rule_static_block.html"


class PageHeaderBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock()

    class Meta:
        group = "header"
        icon = "title"
        template = "home/blocks/page_header_block.html"


class PageHeaderImageBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    image = ImageChooserBlock()

    class Meta:
        group = "header"
        icon = "title"
        template = "home/blocks/page_header_image_block.html"


class SocialStaticBlock(blocks.StaticBlock):

    class Meta:
        admin_text = "Displays list of all Social Link snippets."
        icon = "group"
        template = "home/blocks/social_static_block.html"


# StreamBlocks
class ContentStreamBlock(blocks.StreamBlock):
    page_header = PageHeaderBlock()
    page_header_with_image = PageHeaderImageBlock()
    horizontal_rule = HorizontalRuleStaticBlock()
    social_static_block = SocialStaticBlock()
    paragraph_block = blocks.RichTextBlock()


# Pages
class ContentPage(Page):
    body = StreamField(ContentStreamBlock())

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
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
