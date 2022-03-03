from django.urls import path

from . import getState

urlpatterns = [
    path('', getState.index, name='index'),
]