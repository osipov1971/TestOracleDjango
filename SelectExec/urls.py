from django.urls import path
from .views import *

urlpatterns = [
    path('shops/', SelectListView.as_view()),
]
