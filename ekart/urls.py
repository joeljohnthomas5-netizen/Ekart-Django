"""
URL configuration for ekart project.

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
from django.urls import path
from ekartapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),  
    path('profile/',views.profile, name='profile'),
    path('adnhome/',views.adnhome, name='adnhome'),
    path('view_customer/', views.admin_view_customer, name='view_customer'),
    path('open_addproduct/', views.open_addproduct, name='open_addproduct'),
    path('add_products/',views.add_product, name='add_products'),
    path("view_products/", views.view_products, name="view_products"),
    path("view_customer_products/",views.view_customer_products,name="view_customer_products"),
    path("category/", views.category, name="category"),
    path("edit_category/<int:id>/", views.edit_category, name="edit_category"),
    path("delete_category/<int:id>/", views.delete_category, name="delete_category"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("view_cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('order_success/', views.order_success, name='order_success'),
    path('increase_quantity/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('update-order/<int:id>/<str:status>/',views.update_order_status, name='update_order_status'),
    path('admin_orders/', views.admin_orders, name="admin_orders")

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)