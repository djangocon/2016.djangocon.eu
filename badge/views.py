from django.shortcuts import render


def badge(request):
    return render(request, 'badge/badge.html')
