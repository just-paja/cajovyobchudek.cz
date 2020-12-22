from django.urls import path

from .views import catalog, static

app_name = 'website' # noqa
urlpatterns = [
    path('', static.home, name='home'),
    path('kontakt', static.contact, name='contact'),
    path('zbozi', catalog.home, name='catalog'),
    path('zbozi/<str:category>', catalog.category, name='catalog_category'),
]
