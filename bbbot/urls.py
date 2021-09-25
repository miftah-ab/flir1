from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import one, start, RegisterView

urlpatterns = [

    path('register', RegisterView.as_view()),
    path('start', views.start),
    path('one', views.one)
]
