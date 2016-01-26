from django.views import generic

from .models import Question


class FAQListView(generic.ListView):
    template_name = 'faq/list.html'
    model = Question

    def get_queryset(self):
        queryset = super(FAQListView, self).get_queryset()
        return queryset.filter(published=True).order_by('category')
