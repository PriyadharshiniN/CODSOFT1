from django.urls import path
from . import views
 
urlpatterns= [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<cname>/<pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('payment/', views.payment, name='paymentpage'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='ordersuccess'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('buy-now/',views.buy_now, name='buy_now'),
    path('buy_payment/<int:product_id>/<int:qty>/', views.buy_payment, name='buy_payment'),
    
]
   