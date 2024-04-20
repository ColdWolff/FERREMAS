from . import views
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request):
    return render(
        request,
        "index.html",
    )


def hnf(request):
    return render(
        request,
        "hnf.html",
    )