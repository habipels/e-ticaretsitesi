from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from django.contrib import messages
from .forms import *
from site_set.models  import *
from django.contrib.auth.decorators import login_required
def AdminLogin(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                status = "moderator"
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("/yonetim/manager/")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = UserLoginForm()
    content = {"form": form}

    return render(request,"admin_login.html",content)

def admin_anasayfa(request):
    return render(request,"admin_page/index.html")
def custom_logout(request):
    logout(request)
    return redirect("/yonetim/login/")
@login_required
def site_settings_index(request):

    content = {}
    if True:
        logo_ekleme = logo_ekle(request.POST or None,request.FILES or None)
        icon_ekleme= icon_ekle(request.POST or None,request.FILES or None)
        content["logo"] = sayfa_logosu.objects.order_by("-id").all()
        content["logo_ekleme"] = logo_ekleme
        content["icon"] = sayfa_iconu.objects.order_by("-id").all()
        content["icon_ekleme"] = icon_ekleme
        if logo_ekleme.is_valid():

            l = logo_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/siteayarlari")
        if icon_ekleme.is_valid():

            l = icon_ekle.save(commit=False)
            l.save()
            return redirect("/yonetim/siteayarlari")
        return render (request,"admin_page/site_settings.html",content)
    else:
        return redirect("/")

def logo_sil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    sayfa_logosu.objects.filter(id = id).delete()
    return redirect("/yonetim/siteayarlari")

def musteriler(request):
    if True:
        return render(request,"admin_page/ekip.html")

@login_required
def site_settings_index_icon(request):

    content = {}
    if True:

        icon_ekleme= icon_ekle(request.POST or None,request.FILES or None)

        content["icon"] = sayfa_iconu.objects.order_by("-id").all()
        content["icon_ekleme"] = icon_ekleme

        if icon_ekleme.is_valid():

            l = icon_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/siteayarlari")
        return render (request,"admin_page/icon_site_settings.html",content)
    else:
        return redirect("/")

def icon_sil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    sayfa_iconu.objects.filter(id = id).delete()
    return redirect("/yonetim/siteayarlariicon")

@login_required
def telefon_site_settings(request):

    content = {}
    if True:

        Telefon_ekleme= Telefon_ekle(request.POST or None,request.FILES or None)

        content["Telefon"] = numara.objects.order_by("-id").all()
        content["Telefon_ekle"] = Telefon_ekle

        if Telefon_ekleme.is_valid():

            l = Telefon_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/telefonayari")
        return render (request,"admin_page/telefon_site_ayarlari.html",content)
    else:
        return redirect("/")

def Telefon_sil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    numara.objects.filter(id = id).delete()
    return redirect("/yonetim/telefonayari")

@login_required
def email_site_settings(request):

    content = {}
    if True:

        Email_ekleme= Email_ekle(request.POST or None,request.FILES or None)

        content["Email"] = email_adres.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme

        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/emailayari")
        return render (request,"admin_page/email_site_ayarlari.html",content)
    else:
        return redirect("/")

def Email_sil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    email_adres.objects.filter(id = id).delete()
    return redirect("/yonetim/emailayari")

@login_required
def adres_site_settings(request):

    content = {}
    if True:

        Email_ekleme= Adress_ekle(request.POST or None,request.FILES or None)

        content["Adres"] = adres.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme

        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/adresayari")
        return render (request,"admin_page/adress_site.html",content)
    else:
        return redirect("/")

def Adres_sil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    adres.objects.filter(id = id).delete()
    return redirect("/yonetim/adresayari")

@login_required
def facebook_site_settings(request):

    content = {}
    if True:

        Email_ekleme= face_ekle(request.POST or None,request.FILES or None)

        content["medya"] = sosyalmedyaFace.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Facebook"
        content ["sosyalmedyaa"] = "facebook"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/facebookayari")
        return render (request,"admin_page/sosyal_medya_ayari.html",content)
    else:
        return redirect("/")

def facebook(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    sosyalmedyaFace.objects.filter(id = id).delete()
    return redirect("/yonetim/facebookayari")

@login_required
def instagram_site_settings(request):

    content = {}
    if True:

        Email_ekleme= insta_ekle(request.POST or None,request.FILES or None)

        content["medya"] = sosyalmedyaInsgr.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "İnstagram"
        content ["sosyalmedyaa"] = "instagram"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/instagramayari")
        return render (request,"admin_page/sosyal_medya_ayari.html",content)
    else:
        return redirect("/")

def instagram(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    sosyalmedyaFace.objects.filter(id = id).delete()
    return redirect("/yonetim/instagramayari")

@login_required
def linkedin_site_settings(request):

    content = {}
    if True:

        Email_ekleme= linkedin_ekle(request.POST or None,request.FILES or None)

        content["medya"] = sosyalmedyalinkd.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Linkedin"
        content ["sosyalmedyaa"] = "linkedin"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/linkedinayari")
        return render (request,"admin_page/sosyal_medya_ayari.html",content)
    else:
        return redirect("/")

def linkedin(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    sosyalmedyalinkd.objects.filter(id = id).delete()
    return redirect("/yonetim/linkedinayari")


@login_required
def youtube_site_settings(request):

    content = {}
    if True:

        Email_ekleme= youtube_ekle(request.POST or None,request.FILES or None)

        content["medya"] = sosyalmedyayoutube.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Youtube"
        content ["sosyalmedyaa"] = "youtube"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/youtubeayari")
        return render (request,"admin_page/sosyal_medya_ayari.html",content)
    else:
        return redirect("/")

def youtube(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    sosyalmedyayoutube.objects.filter(id = id).delete()
    return redirect("/yonetim/youtubeayari")
@login_required
def twt_site_settings(request):

    content = {}
    if True:

        Email_ekleme= tw_ekle(request.POST or None,request.FILES or None)

        content["medya"] = sosyalmedyatw.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Twitter"
        content ["sosyalmedyaa"] = "twitter"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/twitterayari")
        return render (request,"admin_page/sosyal_medya_ayari.html",content)
    else:
        return redirect("/")

def twiter(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    sosyalmedyatw.objects.filter(id = id).delete()
    return redirect("/yonetim/twitterayari")

@login_required
def isim_site_settings(request):

    content = {}
    if True:

        Email_ekleme= site_isim_ekle(request.POST or None,request.FILES or None)

        content["medya"] = site_adi.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Siteye İsim "
        content ["sosyalmedyaa"] = "siteismisil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/isimayari")
        return render (request,"admin_page/site_isim_ayari.html",content)
    else:
        return redirect("/")

def siteismisil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    site_adi.objects.filter(id = id).delete()
    return redirect("/yonetim/isimayari")


@login_required
def seo_site_settings(request):

    content = {}
    if True:

        Email_ekleme= site_seo_ekle(request.POST or None,request.FILES or None)

        content["medya"] = seo_ayarlari.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Site Seo Ayarları "
        content ["sosyalmedyaa"] = "seosil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/seoayari")
        return render (request,"admin_page/seo_site_ayarlari.html",content)
    else:
        return redirect("/")

def seosil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    seo_ayarlari.objects.filter(id = id).delete()
    return redirect("/yonetim/seoayari")

@login_required
def banner_site_settings(request):

    content = {}
    if True:

        Email_ekleme= site_banner_ekle(request.POST or None,request.FILES or None)

        content["medya"] = banner.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Site Banner Ayarları "
        content ["sosyalmedyaa"] = "bannersil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/bannerayari")
        return render (request,"admin_page/banner_site_ayarlari.html",content)
    else:
        return redirect("/")

def bannersil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    banner.objects.filter(id = id).delete()
    return redirect("/yonetim/bannerayari")
def bannerduzenle(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    bannner_duzenle = get_object_or_404(banner,id = id)
    form = site_banner_ekle(request.POST or None,request.FILES or None,instance = bannner_duzenle)
    content = {}
    content["Email_ekle"] = form
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        return redirect("/yonetim/bannerayari")
    return render(request,"admin_page/bannerduzenle.html",content)


@login_required
def anasayfa_site_settings(request):

    content = {}
    if True:

        Email_ekleme= anasayfa_ekle(request.POST or None,request.FILES or None)

        content["medya"] = anasayfa.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Anasayfa Metin Ayarları "
        content ["sosyalmedyaa"] = "anasayfasil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/anasayfaayari")
        return render (request,"admin_page/anasayfa_site_ayari.html",content)
    else:
        return redirect("/")

def anasayfasil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    anasayfa.objects.filter(id = id).delete()
    return redirect("/yonetim/anasayfaayari")

@login_required
def hakkimizda_site_settings(request):

    content = {}
    if True:

        Email_ekleme= hakkimizda_ekle(request.POST or None,request.FILES or None)

        content["medya"] = hakkimizda.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Hakkımızda Metin Ayarları "
        content ["sosyalmedyaa"] = "hakkimizdasil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/hakkimizdaayari")
        return render (request,"admin_page/anasayfa_site_ayari.html",content)
    else:
        return redirect("/")

def hakkimizdasil(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    hakkimizda.objects.filter(id = id).delete()
    return redirect("/yonetim/hakkimizdaayari")

@login_required
def gomuluadres_site_settings(request):

    content = {}
    if True:

        Email_ekleme= gomuluadres_ekle(request.POST or None,request.FILES or None)

        content["medya"] = gomulu_adres.objects.order_by("-id").all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Gömülüadres"
        content ["sosyalmedyaa"] = "gomuluadress"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/gomuluadres")
        return render (request,"admin_page/gomulu.html",content)
    else:
        return redirect("/")

def gomuluadress(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    gomulu_adres.objects.filter(id = id).delete()
    return redirect("/yonetim/gomuluadres")


@login_required
def kategori_settings(request):

    content = {}
    if True:

        Email_ekleme= kategori_ekle(request.POST or None,request.FILES or None)

        content["medya"] = Meslek.objects.order_by("-id").filter(silinme_bilgisi =False).all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Kategori"
        content ["sosyalmedyaa"] = "kategorisil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/kategori")
        return render (request,"admin_page/kategori.html",content)
    else:
        return redirect("/")

def kategorisil (request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    Meslek.objects.filter(id = id).update(silinme_bilgisi = True)
    return redirect("/yonetim/kategori")
def kategori_urun_gosterduzenle(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    bannner_duzenle = get_object_or_404(Meslek,id = id)
    form = kategori_ekle(request.POST or None,request.FILES or None,instance = bannner_duzenle)
    content = {}
    content["Email_ekle"] = form
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        return redirect("/yonetim/kategori")
    return render(request,"admin_page/bannerduzenle.html",content)
def filtre_urun_gosterduzenle(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    bannner_duzenle = get_object_or_404(filtre,id = id)
    form = filtre_ekle(request.POST or None,request.FILES or None,instance = bannner_duzenle)
    content = {}
    content["Email_ekle"] = form
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        return redirect("/yonetim/filtreayarlari")
    return render(request,"admin_page/bannerduzenle.html",content)

def filtre_icerigisil(request,id):
    filtre_icerigi.objects.filter(id = id).delete()
    return redirect("/yonetim/filtreayarlari")

@login_required
def urun_ekle_settings(request):

    content = {}
    if True:

        Email_ekleme= urun_ekle(request.POST or None,request.FILES or None)

        content["medya"] = urun.objects.order_by("-id").filter(silinme_bilgisi =False).all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Ürün"
        content ["sosyalmedyaa"] = "urunsil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/urunekle")
        return render (request,"admin_page/urun_ekleme.html",content)
    else:
        return redirect("/")
@login_required
def urun_ekleme_yap(request):

    content = {}
    if True:

        Email_ekleme= urun_ekle(request.POST or None,request.FILES or None)

        content["medya"] = urun.objects.order_by("-id").filter(silinme_bilgisi =False).all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Ürün"
        content ["sosyalmedyaa"] = "urunsil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            Email_ekleme.save_m2m()
            x = "/yonetim/urunfiltre/"+str(l.id)
            return redirect(x)
        return render (request,"admin_page/filtreye_icerik_ekle.html",content)
    else:
        return redirect("/")
def urun_filre_ve_resim_ekleme(request,id):
    content = {}
    form = MultipleImageUploadForm(request.POST, request.FILES)
    content["form"] =form
    urun_bilgisi =get_object_or_404(urun,id = id)
    kategorileri = []
    filtreler =[] 
    tum_kategoriler = []
    a = urun_bilgisi.kategori.all()
    for i in a :
        kategorileri.append(i)
    for i in kategorileri:
        z = i
        while z:    
            if z.ust_kategory :
                tum_kategoriler.append(z.id)
            else:
                tum_kategoriler.append(z.id)
            z =  z.ust_kategory
    file = filtre.objects.filter(filtre_bagli_oldu_kategori__id__in = tum_kategoriler)
    if request.POST:
        if form.is_valid():
            images = request.FILES.getlist('images')
            for images in images:
                urun_resimleri.objects.create(image=images,urun_bilgisi = get_object_or_404(urun,id = id))  # Urun_resimleri modeline resimleri kaydet
        for j in file:
            if request.POST.get(j.filtre_linki):
                urun_filtre_tercihi.objects.create(urun = get_object_or_404(urun,id = id),filtre_bilgisi = get_object_or_404(filtre_icerigi,id = request.POST.get(j.filtre_linki)))
            print(request.POST.get(j.filtre_linki))
        return redirect("/yonetim/urunekle") 
    content["fil"] = tum_kategoriler
    content["filtreler"] = file
    content["kategoriler"] = kategorileri
    return render (request,"admin_page/urun_alt_ozellik.html",content)
def urunsil (request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    urun.objects.filter(id = id).update(silinme_bilgisi = True)
    return redirect("/yonetim/urunekle")
def urun_kategori_bazli_fiyat_degisikligi(request):

    content = {}
    content["kategoriler"] = Meslek.objects.order_by("-id").filter(silinme_bilgisi =False).all()
    if request.POST:
        kategorisi = request.POST.get("kategorisi")
        fiyatdurum = request.POST.get("fiyatdurum")
        oran = float(request.POST.get("oran"))
        if kategorisi == "0":
            tum_urun = urun.objects.all()
        else:
            tum_urun = urun.objects.filter(kategori__id = kategorisi)
        if fiyatdurum == "1":
            urun_fiyat = 0
            for i in tum_urun:
                id = i.id
                urun_fiyat = i.fiyat
                a = i.fiyat
                urun_fiyat = ((urun_fiyat *oran)/100)+urun_fiyat
                urun.objects.filter(id = id).update(fiyat = urun_fiyat,eski_fiyat = a)
        else:
            urun_fiyat = 0
            for i in tum_urun:
                id = i.id
                urun_fiyat = i.fiyat
                a = i.fiyat
                urun_fiyat = urun_fiyat-((urun_fiyat *oran)/100)
                urun.objects.filter(id = id).update(fiyat = urun_fiyat,eski_fiyat = a)
        return redirect("/yonetim/urunekle")
    return render (request,"admin_page/kategori_bazli_fiyat_destirme.html",content)
@login_required
def stogu_ondan_az_urunler_settings(request):

    content = {}
    if True:

        Email_ekleme= urun_ekle(request.POST or None,request.FILES or None)

        content["medya"] = urun.objects.order_by("-id").filter(silinme_bilgisi =False,urun_stok__lt=10).all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Ürün"
        content ["sosyalmedyaa"] = "urunsil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.save()
            return redirect("/yonetim/urunekle")
        return render (request,"admin_page/urun_ekleme.html",content)
    else:
        return redirect("/")
@login_required
def filtre_settings(request):

    content = {}
    if True:

        Email_ekleme= filtre_ekle(request.POST or None,request.FILES or None)

        content["medya"] = filtre.objects.order_by("-id").filter(silinme_bilgisi =False).all()
        content["Email_ekle"] = Email_ekleme
        content["sosyalmedya"] = "Filtre"
        content ["sosyalmedyaa"] = "filtresil"
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.filtre_linki = l.filtre_adi
            l.save()
            return redirect("/yonetim/filtreayarlari")
        return render (request,"admin_page/filtre_ayarlari.html",content)
    else:
        return redirect("/")

def filtresil (request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    filtre.objects.filter(id = id).update(silinme_bilgisi = True)
    return redirect("/yonetim/filtreayarlari")

def filtreye_icerik_ekle(request,id):

    content = {}
    if True:

        Email_ekleme= filtre_icerigi_ekle(request.POST or None,request.FILES or None)
        content["Email_ekle"] = Email_ekleme
        if Email_ekleme.is_valid():

            l = Email_ekleme.save(commit=False)
            l.filtre_bagli_oldu_filtre = get_object_or_404(filtre,id = id)
            l.save()
            x = "/yonetim/filtreyeicerikekle/"+str(id)
            return redirect(x)
        return render (request,"admin_page/filtreye_icerik_ekle.html",content)
    else:
        return redirect("/")
    return render(request,"filtreye_icerik_ekle.html",content)

def yasal_metin_ekleme(request):
    content = {}

    if True:

        Email_ekleme= yasal_ekle(request.POST or None,request.FILES or None)

        content["Email"] = yasal_metinler.objects.order_by("-id").all()  
    return render(request,"admin_page/yasal_metin.html",content)

def yasal_metin_ekle(request):

    content = {}
    if True:
        pass
    else:
        return redirect("/")

    form = yasal_ekle(request.POST or None,request.FILES or None)
    content = {}
    content["Email_ekle"] = form
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        return redirect("/yonetim/yasalmetin")
    return render(request,"admin_page/bannerduzenle.html",content)

def yasal_metin_sil(request,id):
    yasal_metinler.objects.filter(id = id).delete()
    return redirect("/yonetim/yasalmetin")


def satin_alinan_siparisler(request):
    if True:
        content = {}
        content["alinan_siparisler"] = satin_alinanlar.objects.all().order_by("-id")
        return render(request,"admin_page/alinan_siparisler.html",content)
def korgolanan_tumsiparisler(request):
    if True:
        content = {}
        content["alinan_siparisler"] = satin_alinanlar.objects.exclude(kargo = None).order_by("-id")
        return render(request,"admin_page/alinan_siparisler.html",content) 
def korgolanmayi_bekleyen (request):
    if True:
        content = {}
        content["alinan_siparisler"] = satin_alinanlar.objects.filter(kargo = None).order_by("-id")
        return render(request,"admin_page/alinan_siparisler.html",content) 
def korgolamaislemi(request,id):

    content = {}
    if True:
        pass
    else:
        return redirect("/")
    bannner_duzenle = get_object_or_404(satin_alinanlar,id = id)
    form = kargola(request.POST or None,request.FILES or None,instance = bannner_duzenle)
    content = {}
    content["Email_ekle"] = form
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        return redirect("/yonetim/satinalinansiparisler")
    return render(request,"admin_page/bannerduzenle.html",content)