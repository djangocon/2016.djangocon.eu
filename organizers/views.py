from django.views import generic

from .models import Organizer


class ListView(generic.ListView):
    template_name = 'organizers/list.html'
    model = Organizer

    def get_queryset(self):
        queryset = super(ListView, self).get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.published()

        return queryset
