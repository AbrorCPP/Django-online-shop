from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name = "home_page"),
    path('login/', views.login_page, name = "login_page"),
    path('register/', views.register_page, name = "register_page"),
    path('logout/', views.logout_view, name = "logout"),
    path('add_product/', views.add_product, name = "add_product"),
    path("products/", views.product_list, name = "product_list"),
]


