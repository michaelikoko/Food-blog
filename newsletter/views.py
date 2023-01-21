from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from newsletter.models import Subscriber
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

class NewsletterView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({"error":"email already exists"}, status=409)
        else:
            subscriber = Subscriber(email=email)
            subscriber.save()
            try:
                current_site = get_current_site(self.request)
                subject = f"Thank you for subscribing to our Newsletter"

                context = {
                    "domain": current_site.domain,
                    "site_name": "9ja Food Blog",
                    "protocol": "http",
                    "subscriber": subscriber
                }
                print(current_site.domain)
                message = get_template('newsletter/newsletter_subscription_email.html').render(context)
                email_message = EmailMessage( subject, message, to=[email,])
                email_message.content_subtype ="html" # Main content is now text/html
                email_message.send()
            except Exception as e:
                print(e)
                subscriber.delete()
                return JsonResponse({"error":"Invalid email address"}, status=400)
        return JsonResponse({"response":"hello world"})


