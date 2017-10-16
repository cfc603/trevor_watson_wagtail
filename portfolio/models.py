# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from .blocks import ContentStreamBlock


class ProjectImageCarousel(Orderable):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    parent = ParentalKey("ProjectPage", related_name="carousel_images")

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("title", classname="full"),
        FieldPanel("subtitle", classname="full"),
    ]


class ProjectLink(Orderable):
    url = models.URLField()
    display_text = models.CharField(max_length=255)
    parent = ParentalKey("ProjectPage", related_name="links")

    panels = [
        FieldPanel("url"),
        FieldPanel("display_text"),
    ]


class ProjectPage(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    body = StreamField(ContentStreamBlock())
    date = models.DateField()
    tags = ClusterTaggableManager(through="ProjectTag", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        MultiFieldPanel([
            FieldPanel("date"),
            FieldPanel("tags"),
        ], heading="Project Information"),
        StreamFieldPanel("body"),
        InlinePanel("carousel_images"),
        InlinePanel("links"),
    ]

    def get_main_image(self):
        try:
            return self.carousel_images.first().image
        except AttributeError:
            return None


class ProjectTag(TaggedItemBase):
    content_object = ParentalKey("ProjectPage", related_name="tagged_items")
