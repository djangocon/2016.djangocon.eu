from django.shortcuts import render

from sponsors.models import Sponsor


def home(request):
    if request.user.is_staff:
        sponsors = Sponsor.objects.all()
    else:
        sponsors = Sponsor.objects.live()
    return render(request, 'home.html', {
        'sponsors': sponsors,
    })


def coc(request):
    return render(request, 'coc.html')


def venue(request):
    return render(request, 'venue.html')


def live(request):
    return render(request, 'live.html')
