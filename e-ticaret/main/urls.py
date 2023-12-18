from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("urun/<int:id>/<str:slug>", views.urunler_tekli_sayfa, name="urunler_tekli_sayfa"),
    path("sepet/<int:id>/<str:slug>", views.sepete_urun_ekleme, name="sepete_urun_ekleme"),
    path("sepetebak", views.sepet_git, name="sepet_git"),
    path("sepetteekle/<int:id>/<str:slug>", views.sepete_urun_ekleme_sepette, name="sepete_urun_ekleme_sepette"),
    path("sepettesil/<int:id>/<str:slug>", views.sepete_urun_ekleme_sepette_azaltma, name="sepete_urun_ekleme_sepette_azaltma"),
]

#