from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.list import BaseListView

from .forms import BulkUploadForm
from .models import Speaker, Talk


class BulkUploadView(UserPassesTestMixin, generic.FormView):
    template_name = 'speakers/bulk_upload.html'
    success_url = reverse_lazy('admin:speakers_speaker_changelist')
    form_class = BulkUploadForm

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        inserted, skipped = form.save()
        messages.success(self.request, "Successfully imported %d speakers (%d skipped)" % (inserted, skipped))
        return super(BulkUploadView, self).form_valid(form)


class ListView(generic.ListView):
    template_name = 'speakers/list.html'
    model = Speaker

    def get_queryset(self):
        queryset = super(ListView, self).get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)
        return queryset


class DetailView(generic.DetailView):
    template_name = 'speakers/detail.html'
    model = Speaker
    context_object_name = 'speaker'


class ScheduleView(generic.ListView):
    template_name = 'speakers/schedule.html'
    model = Talk

    def get_queryset(self):
        queryset = super(ScheduleView, self).get_queryset()
        queryset = queryset.select_related('speaker')
        return queryset


class ScheduleIcalView(BaseListView):
    model = Talk

    def render_to_response(self, context):
        calendar = self.object_list.as_ical()
        return HttpResponse(calendar.to_ical(),
                            content_type='text/calendar; charset=UTF-8')
