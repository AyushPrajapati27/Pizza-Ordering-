"""
URL configuration for pizza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',home,name='home'),
    path('login/',login_page,name='login_page'),
    path('register/',register_page,name='register_page'),
    path('add-cart/<pizza_uid>',add_cart,name='add_cart'),
    path('cart/',cart,name='cart'),
    path('remvove-cart-items/<cart_item_uid>/',remove_cart_items,name='remove_cart_items'),
    path('orders/',orders,name='orders'),
    path('success/<uuid:uuid>',success,name='success'),
    path('logout/',user_logout,name='user_logout'),
    path('search/',pizza_list,name='pizza_list'),
    path("wishlist/",wishlist,name="wishlist"),
    path("wishlist/add/<str:pizza_name>",add_to_wishlist,name="add_to_wishlist"),
    path("wishlist/remove/<str:pizza_name>",remove_from_wishlist,name="remove_from_wishlist"),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

