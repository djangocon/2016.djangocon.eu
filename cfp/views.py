from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views import generic

from .forms import CfpForm
from .models import Proposal


class LandingView(generic.TemplateView):
    template_name = 'cfp/landing.html'


class CreateView(generic.CreateView):
    model = Proposal
    template_name = 'cfp/propose.html'
    form_class = CfpForm
    success_url = reverse_lazy('cfp:thanks')
    http_method_names = ['get', 'options']  # POST disabled because cfp is closed


class ThankYouView(generic.TemplateView):
    template_name = 'cfp/thanks.html'
