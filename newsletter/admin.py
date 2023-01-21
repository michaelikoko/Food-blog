from django.contrib import admin

# Register your models here.
from newsletter.models import Subscriber

admin.site.register(Subscriber)