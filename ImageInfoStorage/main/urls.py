from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('show', views.show_page, name="show_page")
]