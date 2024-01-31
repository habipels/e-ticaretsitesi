from django.contrib import admin
from django.urls import path
from urun import views

app_name = "user"

urlpatterns = [
    path('register/',views.register,name = "register"),
    path('login/',views.loginUser,name = "login"),
    path('logout/',views.logoutUser,name = "logout"),
    path('girisyap/',views.login_yaptir,name = "login_yaptir"),
    path('kayityap/',views.kayit_ol,name = "kayit_ol"),
]