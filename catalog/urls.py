from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import IndexView, ProductListView, ContactView, ProductDetailView, RecordListView, RecordDetailView, \
    RecordCreateView, RecordUpdateView, RecordDeleteView, CategoriesListView, VersionListView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView
from users.views import ProfileUpdateView, RegisterView

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('categories/', CategoriesListView.as_view(), name='categories_list'),
    path('version/', VersionListView.as_view(), name='version_list'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_item'),
    path('product/create/', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('product/update/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product_update'),
    path('product/delete/<int:pk>/', never_cache(ProductDeleteView.as_view()), name='product_delete'),
    path('records/', RecordListView.as_view(), name='records_list'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/create/', never_cache(RecordCreateView.as_view()), name='record_create'),
    path('record/update/<int:pk>/', never_cache(RecordUpdateView.as_view()), name='record_update'),
    path('record/delete/<int:pk>/', never_cache(RecordDeleteView.as_view()), name='record_delete'),
]
