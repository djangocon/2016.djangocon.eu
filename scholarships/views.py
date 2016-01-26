from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.views import generic

from djangocon.csvutils import StreamingCSVDownloadView
from .forms import ApplicationForm
from .models import Application


class LandingView(generic.CreateView):
    model = Application
    template_name = 'scholarships/landing.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('scholarships:thanks')
    http_method_names = ['get', 'options']  # POST disabled because applications are closed


class ThankYouView(generic.TemplateView):
    template_name = 'scholarships/thanks.html'


class ApplicationsDownloadView(UserPassesTestMixin, StreamingCSVDownloadView):
    def test_func(self):
        return self.request.user.is_staff

    def get_rows(self):
        yield Application.as_csv_row.HEADER
        for application in Application.objects.order_by('submitted_on'):
            yield application.as_csv_row()

    def get_filename(self):
        return 'applications-{:%Y%m%d_%H%M%S}.csv'.format(timezone.now())
