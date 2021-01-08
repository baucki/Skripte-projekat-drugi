from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('cart', views.cart, name='cart'),
    path('/cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('/cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('/buy', views.buy, name="buy"),
    path('/add', views.add, name='add'),
    path('/delete/<int:id>/', views.delete, name='delete')

]