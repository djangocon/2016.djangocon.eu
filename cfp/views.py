from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

from djangocon.csvutils import StreamingCSVDownloadView
from .forms import CfpForm, WorkshopForm
from .models import Proposal, WorkshopProposal


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


class ProposalDownloadView(UserPassesTestMixin, StreamingCSVDownloadView):
    def test_func(self):
        return self.request.user.is_staff

    def get_rows(self):
        anonymized = self.request.GET.get('anonymized', 'true') == 'true'
        yield Proposal.as_csv_row.HEADER
        for proposal in Proposal.objects.order_by('submitted_on'):
            yield proposal.as_csv_row(anonymized=anonymized)

    def get_filename(self):
        return 'proposals-{:%Y%m%d_%H%M%S}.csv'.format(timezone.now())


class ProposeWorkshopView(generic.CreateView):
    template_name = "cfp/propose_workshop.html"
    model = WorkshopProposal
    form_class = WorkshopForm
    success_url = reverse_lazy('cfp:thanks')
    http_method_names = ['get', 'options']  # POST disabled because cfp is closed
