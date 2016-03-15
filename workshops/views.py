from django.views import generic
from django.views.generic.list import BaseListView

from .models import Workshop


class ScheduleView(generic.ListView):
    template_name = 'workshops/schedule.html'
    model = Workshop


class ScheduleIcalView(BaseListView):
    model = Workshop

    def render_to_response(self, context):
        calendar = self.object_list.as_ical()
        return HttpResponse(calendar.to_ical(),
                            content_type='text/calendar; charset=UTF-8')
