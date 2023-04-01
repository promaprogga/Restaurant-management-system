from django.urls import path

from Product_App import views

app_name = 'Product_App'

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation/<int:id>', views.reservation, name='reservation'),
    path('ur_reserve/', views.ur_reserve, name='ur_reserve'),
    path('menus/<int:id>', views.menu_list, name='menus'),
    path('orders/', views.orders, name='orders'),

    # Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/<int:id>', views.cart_detail, name='cart_detail'),
]
