from django.db import models

# Create your models here.
from django import forms
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from modelcluster.fields import ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from wagtail.search import index

class RecipeIndexPage(Page):
    title_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_image")
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = ['recipe.RecipePage']

    def get_context(self, request, *args, **kwargs):
        """ Overiding context to add pagination """
        context = super().get_context(request, *args, **kwargs)

        #Get all categories
        categories = RecipeCategory.objects.all()
        context["categories"] = categories

        category = request.GET.get("category", None)
        if category:
            #Filter the recipes
            all_recipes = RecipePage.objects.live().filter(categories__category_name=category)
            context["category"] = category
        else:
            # Get all recipes
            all_recipes = RecipePage.objects.live().order_by("-first_published_at")
        
        #print(all_recipes, len(all_recipes))
        # Paginate all recipes by 15 per page
        paginator = Paginator(all_recipes, 15)

        # Try to get the ?page=x value
        page = request.GET.get("page", 1)

        try:
            # If the page exists and the ?page=x is an int
            recipes = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            recipes = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            recipes = paginator.page(paginator.num_pages)

        context["recipes"] = recipes
        return context

class IngredientBlock(blocks.StructBlock):
    ingredient = blocks.CharBlock(max_length=255)
    handy_measure = blocks.CharBlock(max_length=255, required=False)
    metric = blocks.CharBlock(max_length=20, required=False)

class RecipeContentBlock(blocks.StructBlock):
    ingredients = blocks.ListBlock(IngredientBlock())
    body = blocks.RichTextBlock()

    class Meta:
        block_counts = {
            'ingredients': {'min_num': 0, 'max_num': 50},
        }

class RecipePage(Page, index.Indexed):
    recipe_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    recipe_title = models.CharField(max_length=255)
    recipe_title_text = models.CharField(max_length=150, blank=True)
    recipe_content = StreamField([
        ("content", RecipeContentBlock())
    ], use_json_field=True, min_num=1, max_num=1)
    date = models.DateField("Post Date", auto_now=True)
    categories = ParentalManyToManyField("recipe.RecipeCategory", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("recipe_image"),
        FieldPanel("recipe_title"),
        FieldPanel("recipe_title_text"),
        FieldPanel("recipe_content"),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
    ]

    parent_page_types = ['recipe.RecipeIndexPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField("recipe_title", partial_match=True),
        index.SearchField("recipe_title_text", partial_match=True),
        index.RelatedFields("categories", [
            index.SearchField("category_name", partial_match=True),
            index.FilterField("category_name")
        ]),
        #index.AutocompleteField("recipe_title"),
        #index.AutocompleteField("recipe_title_text")
    ]

    def get_absolute_url(self):
        return self.get_url()

@register_snippet
class RecipeCategory(models.Model):
    category_name = models.CharField(max_length=255)
    category_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("category_name"),
        FieldPanel("category_icon")
    ]

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'recipe categories'