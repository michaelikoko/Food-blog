from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin
from birdsong.options import CampaignAdmin

from newsletter.models import NewsletterEmail, Subscriber


@modeladmin_register
class NewsletterEmailAdmin(CampaignAdmin):
    campaign = NewsletterEmail
    menu_label = 'Newsletter Email'
    menu_icon = 'mail'
    menu_order = 200
    contact_class = Subscriber


# You may want to add your own modeladmin here to list/edit/add contacts
@modeladmin_register
class SubscriberAdmin(ModelAdmin):
    model = Subscriber
    menu_label = 'Subscribers'
    menu_icon = 'user'
    list_diplay = ('email', )