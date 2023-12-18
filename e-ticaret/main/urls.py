from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("urun/<int:id>/<str:slug>", views.urunler_tekli_sayfa, name="urunler_tekli_sayfa"),
    path("sepet/<str:slug>", views.sepete_urun_ekleme, name="sepete_urun_ekleme"),
]
#