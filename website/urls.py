from django.urls import path

from .views import catalog, contact, static

app_name = 'website' # noqa
urlpatterns = [
    path('', static.home, name='home'),
    path('kontakt', contact.home, name='contact'),
    path('katalog', catalog.home, name='catalog'),
    path('katalog/<str:tag_id>', catalog.tag, name='catalog_tag'),
]
