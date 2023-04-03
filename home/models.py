from django.db import models

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from modelcluster.fields import ParentalKey
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from recipe.models import RecipePage

class HomePage(Page):
    hero_carousel_text = StreamField([
        ("text", blocks.CharBlock()),
    ], use_json_field=True, min_num=1, max_num=3)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_carousel_text"),
            InlinePanel("carousel_images", label="Hero Carousel Images", min_num=2, max_num=3),
        ], heading="Hero Section")
    ]

    #parent_page_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        #Get 6 latest recipes
        latest_recipes = RecipePage.objects.all().order_by("-first_published_at")[:6]
        context["latest_recipes"] = latest_recipes
        return context
    
class HeroCarouselImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="carousel_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+"
    )

    panels = [
        FieldPanel("page"),
        FieldPanel("image")
    ]

class AboutContentBlock(blocks.StructBlock):
    content_text = blocks.TextBlock()
    content_image = ImageChooserBlock()

class AboutPage(Page):
    title_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    body = StreamField([
        ("content", AboutContentBlock())
    ], use_json_field=True, min_num=1, max_num=1)

    content_panels = Page.content_panels + [
        FieldPanel("title_image"),
        FieldPanel("body")
    ]

    parent_page_types = ['HomePage']
    subpage_types = []

class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")

class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    title_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
        FieldPanel("title_image"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("from_address", classname="col6"),
                FieldPanel("to_address", classname="col6")
            ]),
            FieldPanel("subject")
        ], "Email")
    ]

    parent_page_types = ['HomePage']
    subpage_types = []