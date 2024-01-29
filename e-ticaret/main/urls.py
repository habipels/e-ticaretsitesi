from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("urun/<int:id>/<str:slug>", views.urunler_tekli_sayfa, name="urunler_tekli_sayfa"),
    path("sepet/<int:id>/<str:slug>", views.sepete_urun_ekleme, name="sepete_urun_ekleme"),
    path("sepetebak", views.sepet_git, name="sepet_git"),
    path("sepetteekle/<int:id>/<str:slug>", views.sepete_urun_ekleme_sepette, name="sepete_urun_ekleme_sepette"),
    path("sepettesil/<int:id>/<str:slug>", views.sepete_urun_ekleme_sepette_azaltma, name="sepete_urun_ekleme_sepette_azaltma"),
    path("urunsil/<int:id>/<str:slug>", views.sepete_urun_ekleme_sepette_silme, name="sepete_urun_ekleme_sepette_silme"),
    path("kategori/<int:id>/<str:slug>/", views.kategori_ver_urunleri_gosterme, name="kategori_ver_urunleri_gosterme"),
    path("odeme", views.odeme_sayfasi, name="odeme_sayfasi"),
    path("hakkimizda", views.hakkimizda_sayfasi, name="hakkimizda_sayfasi"),
    path("urunekle/", views.sepete_urun_ekleme_toplu, name="sepete_urun_ekleme_toplu"),
    path("yasalmetinler/<int:id>/<str:slug>", views.yasal_metinler_sayfasi, name="yasal_metinler_sayfasi"),
    path("iletisim", views.iletisim_sayfasi, name="iletisim_sayfasi"),
    path("odeme/bilgilerikaydet/", views.odeme_sayfasi_bilgileri_kaydet, name="odeme_sayfasi_bilgileri_kaydet"),
    path("odeme/havale/", views.havale_sayfasi, name="havale_sayfasi"),
    path("havale/havale/", views.success, name="success"),
    path("indirimdeolanurunler/", views.indirimli_urunleri_gosterme, name="indirimli_urunleri_gosterme"),
]
#