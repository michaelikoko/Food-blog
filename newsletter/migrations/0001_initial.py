# Generated by Django 4.1.5 on 2023-03-17 23:10

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    #dependencies = [
    #    ('birdsong', '0007_alter_contacttag_tag'),
    #]

    operations = [
        migrations.CreateModel(
            name='NewsletterEmail',
            fields=[
                ('campaign_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='birdsong.campaign')),
                ('body', wagtail.fields.StreamField([('body', wagtail.blocks.StructBlock([('body', wagtail.blocks.StreamBlock([('rich_text', wagtail.blocks.RichTextBlock(features=['h3', 'h4', 'bold', 'italic', 'link', 'ul', 'ol', 'document-link'], template='birdsong/mail/blocks/richtext.html'))])), ('linked_recipes', wagtail.blocks.ListBlock(wagtail.blocks.PageChooserBlock(page_type=['recipe.RecipePage'], required=False)))]))], use_json_field=True)),
            ],
            bases=('birdsong.campaign',),
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('contact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='birdsong.contact')),
            ],
            options={
                'abstract': False,
            },
            bases=('birdsong.contact',),
        ),
    ]
