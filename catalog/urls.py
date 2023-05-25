from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contacts, name='contact'),
    path('home/', home, name='home'),
    path('product/', product, name='pr_pg'),
    path('product/<pk>/', product, name='product'),
]
