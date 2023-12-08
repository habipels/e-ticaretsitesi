from django.urls import path
from . import views
app_name = "admin_panels"
urlpatterns = [
    path("login/",views.AdminLogin,name="AdminLogin"),
    path("manager/",views.admin_anasayfa,name="admin_anasayfa"),
    path("logout",views.custom_logout,name="custom_logout"),

    path("siteayarlariicon",views.site_settings_index_icon,name="site_settings_index_icon"),
    path("siteayarlari",views.site_settings_index,name="siteayarlari"),
    path("telefonayari",views.telefon_site_settings,name="telefon_site_settings"),
    path("emailayari",views.email_site_settings,name="email_site_settings"),
    path("adresayari",views.adres_site_settings,name="adres_site_settings"),
    path("facebookayari",views.facebook_site_settings,name="facebook_site_settings"),
    path("instagramayari",views.instagram_site_settings,name="instagram_site_settings"),
    path("linkedinayari",views.linkedin_site_settings,name="linkedin_site_settings"),
    path("youtubeayari",views.youtube_site_settings,name="youtube_site_settings"),
    path("twitterayari",views.twt_site_settings,name="twt_site_settings"),
    path("isimayari",views.isim_site_settings,name="isim_site_settings"),
    path("seoayari",views.seo_site_settings,name="seo_site_settings"),
    path("bannerayari",views.banner_site_settings,name="banner_site_settings"),
    path("anasayfaayari",views.anasayfa_site_settings,name="anasayfa_site_settings"),
    path("hakkimizdaayari",views.hakkimizda_site_settings,name="hakkimizda_site_settings"),
    path("gomuluadres",views.gomuluadres_site_settings,name="gomuluadres_site_settings"),
    path("kategori",views.kategori_settings,name="kategori_settings"),
    #silme işlemleri
    #
    path("kategorisil/<int:id>",views.kategorisil,name="kategorisil"),
    path("gomuluadress/<int:id>",views.gomuluadress,name="gomuluadress"),
    path("logosil/<int:id>",views.logo_sil,name="logosil"),
    path("iconsil/<int:id>",views.icon_sil,name="iconsil"),
    path("telefonsil/<int:id>",views.Telefon_sil,name="telefonsil"),
    path("emailsil/<int:id>",views.Email_sil,name="emailsil"),
    path("adressil/<int:id>",views.Adres_sil,name="adressil"),
    path("facebook/<int:id>",views.facebook,name="facebook"),
    path("instagram/<int:id>",views.instagram,name="instagram"),
    path("linkedin/<int:id>",views.linkedin,name="linkedin"),
    path("youtube/<int:id>",views.youtube,name="youtube"),
    path("twitter/<int:id>",views.twiter,name="twiter"),
    path("siteismisil/<int:id>",views.siteismisil,name="siteismisil"),
    path("seosil/<int:id>",views.seosil,name="seosil"),
    path("bannersil/<int:id>",views.bannersil,name="bannersil"),
    path("bannerduzenle/<int:id>",views.bannerduzenle,name="bannerduzenle"),
    path("anasayfasil/<int:id>",views.anasayfasil,name="anasayfasil"),
    path("hakkimizdasil/<int:id>",views.hakkimizdasil,name="hakkimizdasil"),
]
#