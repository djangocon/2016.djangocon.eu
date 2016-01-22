from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .forms import BulkUploadForm
from .models import Speaker


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
