from django.urls import path, include
from .views import *

from .chart import funcFdrBarChart

app_name = "SATVAI"

urlpatterns = [
    path('', index, name="index"),
    path('satvai/', satvai, name="satvai"),
    path('brihat/', brihat, name="brihat"),
    path('cpvp/', cpvp, name="cpvp"),
]