from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import IndexView, ProductListView, ContactView, ProductDetailView, RecordListView, RecordDetailView, \
    RecordCreateView, RecordUpdateView, RecordDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_item'),
    path('records/', RecordListView.as_view(), name='records_list'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/create/', RecordCreateView.as_view(), name='record_create'),
    path('record/update/<int:pk>/', RecordUpdateView.as_view(), name='record_update'),
    path('record/delete/<int:pk>/', RecordDeleteView.as_view(), name='record_delete'),
]
