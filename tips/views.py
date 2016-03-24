from django.views.generic import TemplateView


index = TemplateView.as_view(template_name='tips/index.html')

airport = TemplateView.as_view(template_name='tips/airport.html')

money = TemplateView.as_view(template_name='tips/money.html')
