from django import template
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

register = template.Library()

@register.simple_tag
def absolute_unsubscribe_url(contact_id):
    """Returns the absolute path of the unsubscribe url using the sites framework and reverse"""
    print(contact_id, get_current_site(None).domain)
    return f"{get_current_site(None).domain}{reverse('birdsong:unsubscribe', args=(contact_id,))}"

@register.simple_tag
def domain():
    """Returns the domain using the sites framework"""
    print(get_current_site(None).domain)
    return f"{get_current_site(None).domain}"