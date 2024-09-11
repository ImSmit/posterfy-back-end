from django.urls import path
from base.views import product_views as views

urlpatterns = [
    path('', views.getProducts, name="get_products"),
    path('<str:pk>/', views.getProduct, name="get_product"),
]
