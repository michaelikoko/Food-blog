from django.db import models

# Create your models here.
from birdsong.blocks import DefaultBlocks
from birdsong.models import Campaign, Contact
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from recipe.models import RecipePage

class NewsletterContentBlock(blocks.StructBlock):
    body = DefaultBlocks()
    linked_recipes = blocks.ListBlock(blocks.PageChooserBlock(page_type=RecipePage, required=False))

class NewsletterEmail(Campaign):
    body = StreamField([
        ("body", NewsletterContentBlock())
    ], use_json_field=True, min_num=1, max_num=1)

    panels = Campaign.panels + [
        FieldPanel('body'),
    ]

class Subscriber(Contact):
    pass