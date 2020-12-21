from django.urls import path

from . import views

app_name = 'website' # noqa
urlpatterns = [
    path('', views.home, name='home'),
    path('kontakt', views.contact, name='contact'),
]
