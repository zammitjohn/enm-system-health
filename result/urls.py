from django.urls import path

from . import getResponse

urlpatterns = [
    path('', getResponse.index, name='index'),
]