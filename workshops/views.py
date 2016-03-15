from django.views import generic

from .models import Workshop


class DetailView(generic.DetailView):
    template_name = 'workshops/detail.html'
    model = Workshop
