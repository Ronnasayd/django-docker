from django.urls import path,include
from .views import *

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('save/',Save.as_view(),name='save'),
]
