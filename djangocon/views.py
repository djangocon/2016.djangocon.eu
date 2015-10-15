from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def coc(request):
    return render(request, 'coc.html')
