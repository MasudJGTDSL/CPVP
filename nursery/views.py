from django.shortcuts import render

from .models import *
from .import chart


def index(request):
    return render(request, "index.html") 

def satvai(request):
    qs = Satvai.objects.all().order_by("category","price")
    return render(request, "satvai.html", {"context":qs}) 


def brihat(request):
    qs = Brihat.objects.all().order_by("title","price")
    return render(request, "brihat.html", {"context":qs}) 


def cpvp(request):
    qs = CPVP.objects.all().order_by("batch","reg_date","praktony_name")
    return render(request, "cpvp.html", {"context":qs,"chart": chart.funcFdrBarChart()}) 

