"""
URL configuration for hotwheels project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from app import views


# from django.urls import path
# from app import views


urlpatterns = [
    
    path('about/', views.about, name='about'),

    path('admin/', admin.site.urls),
    path('adminlogin/',views.adminlogin),
    path('adminlogin/dashboard',views.adminlist,name='adminlist'),
    path('userlogin/',views.userlogin,name="userlogin"),
    path('logout/',views.logout_view,name="logout"),
    path('addproduct/',views.addproduct,),
    path('product_list/', views.product_list, name='product_list'),
    path('delete/<int:id>/', views.delete_car, name='delete_car'),
    path('userregister/',views.userregister),
    path('catalog/', views.catalog, name='catalog'),
    path('addcart/<int:car_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('user_list/', views.user_list, name='userlist'),
    path('',views.user_page, name='userpage'),
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # Wishlist
    
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('edit/<int:id>/', views.edit_car, name='editcar'),
    path('removewishlist/<int:id>/', views.remove_wishlist, name='remove_wishlist'),


    path('buynow/', views.buy_now, name='buy_now'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
