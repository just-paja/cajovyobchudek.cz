from django.urls import path

from .views import catalog, contact, static

app_name = 'website' # noqa
urlpatterns = [
    path('', static.home, name='home'),
    path('kontakt', contact.home, name='contact'),
    path('zbozi', catalog.home, name='catalog'),
    path('zbozi/<str:category_id>', catalog.category, name='catalog_category'),
]
