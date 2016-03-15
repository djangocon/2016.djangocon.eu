import icalendar

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from speakers.models import Talk
from workshops.models import Workshop


def get_programs():
    return [
        {
            'name': 'Conference',
            'description': 'Three days of talks by a talented bunch of international speakers.\nExpand your horizons into the world of Django and beyond.',
            'venue': 'Budapest Music Center',
            'venue_url': reverse('venue'),
            'events': Talk.objects.select_related('speaker'),
        },
        {
            'name': 'Workshops/Sprints',
            'description': 'Two days of workshops and sprints where you can learn how to contribute to your favorite open source projects.',
            'venue': 'MÜSZI',
            'venue_url': reverse('venue') + '#workshops',
            'events': Workshop.objects.all(),
        },
    ]


class ScheduleView(generic.TemplateView):
    template_name = 'schedule/schedule.html'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['programs'] = get_programs()
        return context


class IcalScheduleView(generic.View):
    def get(self, request):
        calendar = self.get_calendar()
        return HttpResponse(calendar.to_ical(),
                            content_type='text/calendar; charset=UTF-8')

    def get_calendar(self, **kwargs):
        calendar = icalendar.Calendar()
        for k, v in kwargs.items():
            calendar[k] = v

        for program in get_programs():
            for event in program['events']:
                calendar.add_component(event.as_ical())

        return calendar
