from django.urls import path

from . import views

app_name = 'website' # noqa
urlpatterns = [
    path('', views.home, name='home'),
    path('kontakt', views.contact, name='contact'),
    path('zbozi', views.catalog, name='catalog'),
    path('zbozi/<str:category>', views.catalog_category, name='catalog_category'),
]
