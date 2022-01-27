from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from . import helper


urlpatterns = [
    path('', views.hello),
    

]
