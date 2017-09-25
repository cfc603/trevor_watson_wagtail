# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from markdown import markdown
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class CodeBlock(blocks.StructBlock):
    """
    Code Highlighting Block
    """
    LANGUAGE_CHOICES = (
        ("bash", "Bash/Shell"),
        ("css", "CSS"),
        ("django", "Django"),
        ("html", "HTML"),
        ("javascript", "JavaScript"),
        ("mysql", "MySQL"),
        ("nginx", "NGINX"),
        ("php", "PHP"),
        ("python", "Python"),
    )

    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES)
    code = blocks.TextBlock()

    class Meta:
        icon = "code"

    def render(self, value, context):
        src = value["code"].strip("\n")
        lang = value["language"]

        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name(
            "html",
            linenos=None,
            cssclass="codehilite",
            style="default",
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock()

    class Meta:
        template = "portfolio/blocks/image_block.html"


class MarkDownBlock(blocks.TextBlock):
    """ MarkDown Block """

    class Meta:
        icon = "code"

    def render_basic(self, value, context):
        md = markdown(
            value,
            [
                "markdown.extensions.fenced_code",
                "codehilite",
            ],
        )
        return mark_safe(md)


# StreamBlock
class ContentStreamBlock(blocks.StreamBlock):
    content = blocks.RichTextBlock(icon="doc-empty")
    image = ImageBlock(icon="image")
    code = CodeBlock()
    markdown = MarkDownBlock()
