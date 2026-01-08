"""URL маршруты приложения shop."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/<int:id>/', views.buy_item, name='buy_item'),
    path('order/<int:id>/buy/', views.buy_order, name='buy_order'),
    path('success/', views.success_page, name='success'),
    path('cancel/', views.cancel_page, name='cancel'),
]

