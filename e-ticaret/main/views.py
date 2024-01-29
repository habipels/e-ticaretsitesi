from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from site_set.models import *
from urun.models import *
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.db.models.query_utils import Q
from django.db.models import F
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def site_bilgileri():
    sozluk = {}
    sozluk["facebook"] = sosyalmedyaFace.objects.last()
    sozluk["tw"] = sosyalmedyatw.objects.last()
    sozluk["insta"] = sosyalmedyaInsgr.objects.last()
    sozluk["link"] = sosyalmedyalinkd.objects.last()
    sozluk["youtube"] = sosyalmedyayoutube.objects.last()
    sozluk["logo"] = sayfa_logosu.objects.last()
    sozluk["pencere_icon"] = sayfa_iconu.objects.last()
    sozluk["kategoriler"] = Meslek.objects.all()
    sozluk["banner"] = banner.objects.filter(banner_gosterme = True).order_by("banner_sira")
    sozluk["site_adi"] = site_adi.objects.last()
    sozluk["email"] = email_adres.objects.last()
    sozluk["telefon"] = numara.objects.last()
    sozluk["hakkimizda"] = hakkimizda.objects.last()
    sozluk["anasayfa"] = anasayfa.objects.last()
    sozluk["yasal_metinler"] = yasal_metinler.objects.all()
    sozluk["adres"] = adres.objects.last()
    return sozluk
# Create your views here.
def homepage(request):
    content = site_bilgileri()
    profile = urun.objects.filter(urun_stok__gte=1,silinme_bilgisi = False)
    if request.GET.get("search"):
        search = request.GET.get("search")
        profile = urun.objects.filter(Q(urun_adi__icontains = search)  & Q(urun_stok__gte=1),Q(silinme_bilgisi = False) )
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 20) # 6 employees per page
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["indirimdekiurunler"] = urun.objects.filter(urun_stok__gte=1,eski_fiyat__gt=F('fiyat'),silinme_bilgisi = False)
    content["populer"] = urun.objects.filter(urun_stok__gte=1,silinme_bilgisi = False).order_by("-urun_bakma_saysi")
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"index.html",content)
def hakkimizda_sayfasi(request):
    content = site_bilgileri()

    return render(request,"hakkimizda.html",content)
def yasal_metinler_sayfasi(request,id,slug):
    content = site_bilgileri()
    content["yasal_metin"] = get_object_or_404(yasal_metinler,id = id)
    return render(request,"yasal.html",content)
def iletisim_sayfasi(request):
    content = site_bilgileri()
    content["gomulu"] = gomulu_adres.objects.last()
    return render(request,"iletisim.html",content)
def urunler_tekli_sayfa (request,id,slug):
    content = site_bilgileri()
    content["urun_"] = get_object_or_404(urun,id = id)
    a  = get_object_or_404(urun,id = id).urun_bakma_saysi+1
    urun.objects.filter(id = id).update(urun_bakma_saysi = a)
    content["urun_resimleri"] = urun_resimleri.objects.filter(urun_bilgisi = get_object_or_404(urun,id = id))
    return render(request,"urunlist/urun_goster.html",content)


def sepete_urun_ekleme(request,id,slug):
    if request.user.is_authenticated:
        try:
            sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last()
            adet = a.urun_adedi +1
            sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).update(urun_adedi = adet)

        except:
            sepetteki_urunler.objects.create(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    else:
        try:
            sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last()
            adet = a.urun_adedi +1
            sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).update(urun_adedi = adet)
        except:
            sepetteki_urunler.objects.create(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    return redirect("/")

def sepete_urun_ekleme_toplu(request):
    if request.POST:
        b = int(request.POST.get("adet"))
        id = request.POST.get("urun")
        urunadi = request.POST.get("urunadi")
        if request.user.is_authenticated:

            try:
                sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
            except:
                sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)

            try:
                a = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                            urun_bilgisi = get_object_or_404(urun,id = id) ).last()
                adet = a.urun_adedi +b
                sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                            urun_bilgisi = get_object_or_404(urun,id = id) ).update(urun_adedi = adet)

            except:
                sepetteki_urunler.objects.create(urun_adedi =b,kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                            urun_bilgisi = get_object_or_404(urun,id = id) )
        else:
            try:
                sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
            except:
                sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)

            try:
                a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                            urun_bilgisi = get_object_or_404(urun,id = id) ).last()
                adet = a.urun_adedi +b
                sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                            urun_bilgisi = get_object_or_404(urun,id = id) ).update(urun_adedi = adet)
            except:
                sepetteki_urunler.objects.create(urun_adedi =b,kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                            urun_bilgisi = get_object_or_404(urun,id = id) )
    z = "/urun/{}/{}".format(id,urunadi.replace("/",""))
    return redirect(z)

def sepet_git(request):
    content = site_bilgileri()
    if request.user.is_authenticated:
        try:
            sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        veriler = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user).last() )
    else:
        try:
            sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        veriler =sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last() )
    content["sepet_urunleri"] =veriler
    return render(request,"urunlist/sepet.html",content)

def sepete_urun_ekleme_sepette(request,id,slug):
    if request.user.is_authenticated:
        try:
            sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last()
            adet = a.urun_adedi +1
            try:
                sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id,urun_stok__gte = adet) ).update(urun_adedi = adet)
            except:
                pass
        except:
            sepetteki_urunler.objects.create(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    else:
        try:
            sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last()
            adet = a.urun_adedi +1
            try:
                sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id,urun_stok__gte = adet) ).update(urun_adedi = adet)
            except:
                pass
        except:
            sepetteki_urunler.objects.create(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    return redirect("/sepetebak")

def sepete_urun_ekleme_sepette_azaltma(request,id,slug):
    if request.user.is_authenticated:
        try:
            sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last()
            adet = a.urun_adedi -1
            sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).update(urun_adedi = adet)

        except:
            sepetteki_urunler.objects.create(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    else:
        try:
            sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last()
            adet = a.urun_adedi -1
            sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).update(urun_adedi = adet)
        except:
            sepetteki_urunler.objects.create(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    return redirect("/sepetebak")


def sepete_urun_ekleme_sepette_silme(request,id,slug):
    if request.user.is_authenticated:
        try:
            sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last().delete()

        except:
            sepetteki_urunler.objects.create(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    else:
        try:
            sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)

        try:
            a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) ).last().delete()
        except:
            sepetteki_urunler.objects.create(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last(),
                                         urun_bilgisi = get_object_or_404(urun,id = id) )
    return redirect("/sepetebak")

def kategori_ver_urunleri_gosterme(request,id,slug):
    content = site_bilgileri()

    kategorileri = []
    a = get_object_or_404(Meslek,id = id)
    tum_kategoriler = []
    for i in Meslek.objects.filter(silinme_bilgisi = False):
        if a.kategori in i.__str__() :
            tum_kategoriler.append(i.id)
    profile = urun.objects.filter(urun_stok__gte=1,kategori__id__in = tum_kategoriler,silinme_bilgisi = False).distinct()
    if request.GET.get("search"):
        search = request.GET.get("search")
        profile = urun.objects.filter(Q(silinme_bilgisi = False),Q(kategori__id__in = tum_kategoriler)&Q(urun_adi__icontains = search)  & Q(urun_stok__gte=1) ).distinct()
    content["filtre"] = filtre_icerigi.objects.filter(filtre_bagli_oldu_filtre__filtre_adi = "MARKA",filtre_bagli_oldu_filtre__filtre_bagli_oldu_kategori__id__in=tum_kategoriler)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 20) # 6 employees per page
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"kategori/kategori_urun_goster.html",content)

def indirimli_urunleri_gosterme(request):
    content = site_bilgileri()

    profile = urun.objects.filter(urun_stok__gte=1,silinme_bilgisi = False).distinct()
    if request.GET:
        search = request.GET.get("search")
        profile = urun.objects.filter(Q(silinme_bilgisi = False)&Q(urun_adi__icontains = search)  & Q(urun_stok__gte=1,eski_fiyat__gt=F('fiyat')) ).distinct()
    content["filtre"] = filtre_icerigi.objects.filter(filtre_bagli_oldu_filtre__filtre_adi = "MARKA")
    page_num = request.GET.get('page', 1)
    paginator = Paginator(profile, 20) # 6 employees per page
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
            # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
            # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    content["santiyeler"] = page_obj
    content["top"]  = profile
    content["medya"] = page_obj
    return render(request,"kategori/indirimli_urun_goster.html",content)


def odeme_sayfasi(request):
    content = site_bilgileri()
    if request.user.is_authenticated:
        try:
            sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        veriler = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user).last() )
        try:
            a = sepet_sahibi_bilgileri.objects.get(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user).last())
        except:
            a = ""
    else:
        try:
            sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        veriler =sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last() )
        try:
            a = sepet_sahibi_bilgileri.objects.get(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last())
        except:
            a = ""
    content["adresler"] = a
    content["sepet_urunleri"] = veriler
    turkey_cities = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
    "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır",
    "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay",
    "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli",
    "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu",
    "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa",
    "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın",
    "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
    ]
    content["turkey_cities"] =turkey_cities
    return render(request,"odeme/odeme.html",content)


def odeme_sayfasi_bilgileri_kaydet(request):
    if request.POST:
        sepet = str(request.POST.get("sepet"))
        isim = request.POST.get("isim")
        soyisim = request.POST.get("soyisim")
        vergi_kimlik_no = request.POST.get("vergi_kimlik_no")
        eposta = request.POST.get("eposta")
        telefon = request.POST.get("telefon")
        adres = request.POST.get("adres")
        ulke = request.POST.get("ulke")
        sehirler = request.POST.get("sehirler")
        zip_kodu = request.POST.get("zip_kodu")
        payment = request.POST.get("payment")
        faturatipi = request.POST.get("faturatipi")
        if faturatipi == "kurumsal":
            faturatipi = True
        else:
            faturatipi = False
        if "ip" in sepet:
            sepet = sepet.replace("ip","")
            sepet = int(sepet)
            if sepet_sahibi_bilgileri.objects.filter(kayitli_olmayan_kullanici__id = sepet).count() > 0:
                sepet_sahibi_bilgileri.objects.filter(kayitli_olmayan_kullanici = get_object_or_404(sepet_olusturma_ip,id = sepet)).update(
                    isim = isim,soyisim = soyisim,
                    vergi_tc = vergi_kimlik_no,email = eposta,
                    telefon = telefon,adres = adres, ulke = ulke,
                    sehirler = sehirler,
                    zip_kodu = zip_kodu,
                    payment = payment,
                   faturatipi = faturatipi
                )
            else:
                sepet_sahibi_bilgileri.objects.create(
                    kayitli_olmayan_kullanici = get_object_or_404(sepet_olusturma_ip,id = sepet),
                    isim = isim,soyisim = soyisim,
                    vergi_tc = vergi_kimlik_no,email = eposta,
                    telefon = telefon,adres = adres, ulke = ulke,
                    sehirler = sehirler,
                    zip_kodu = zip_kodu,
                    payment = payment,
                   faturatipi = faturatipi
                )
        elif "kayitli" in sepet:
            sepet = sepet.replace("kayitli","")
            sepet = int(sepet)
            if sepet_sahibi_bilgileri.objects.filter(kayitli_kullanici = get_object_or_404(sepet_olusturma,id = sepet)).count() >1:
                sepet_sahibi_bilgileri.objects.filter(kayitli_kullanici = get_object_or_404(sepet_olusturma,id = sepet)).update(
                    isim = isim,soyisim = soyisim,
                    vergi_tc = vergi_kimlik_no,email = eposta,
                    telefon = telefon,adres = adres, ulke = ulke,
                    sehirler = sehirler,
                    zip_kodu = zip_kodu,
                    payment = payment,
                   faturatipi = faturatipi
                )
            else:
                sepet_sahibi_bilgileri.objects.create(
                    kayitli_kullanici = get_object_or_404(sepet_olusturma,id = sepet),
                    isim = isim,soyisim = soyisim,
                    vergi_tc = vergi_kimlik_no,email = eposta,
                    telefon = telefon,adres = adres, ulke = ulke,
                    sehirler = sehirler,
                    zip_kodu = zip_kodu,
                    payment = payment,
                   faturatipi = faturatipi
                )
        if payment == "Havale":
            return redirect("/odeme/havale/")
        else:
            return redirect("/pay/payment/")

def havale_sayfasi(request):
    content = site_bilgileri()
    if request.user.is_authenticated:
        try:
            sepet_olusturma.objects.get(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma.objects.create(sepet_sahibi = request.user,sepet_satin_alma_durumu = False)
        veriler = sepetteki_urunler.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user).last() )
        try:
            a = sepet_sahibi_bilgileri.objects.get(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user).last())
        except:
            a = ""
    else:
        try:
            sepet_olusturma_ip.objects.get(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        except:
            sepet_olusturma_ip.objects.create(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False)
        veriler =sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last() )
        try:
            a = sepet_sahibi_bilgileri.objects.get(kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last())
        except:
            a = ""
    content["adresler"] = a
    content["sepet_urunleri"] = veriler
    turkey_cities = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
    "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır",
    "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay",
    "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli",
    "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu",
    "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa",
    "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın",
    "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
    ]
    content["turkey_cities"] =turkey_cities
    content["banka"] = banka_bilgileri.objects.last()
    return render(request,"odeme/odeme_havale.html",content)
def bugunsiparis():
    bugunku_tarih_ve_saat = datetime.now()
    a =satin_alinanlar.objects.filter(kayit_tarihi__gte=bugunku_tarih_ve_saat.replace(hour=0, minute=0, second=0, microsecond=0)).count()
    b = str(bugunku_tarih_ve_saat.day)+str(bugunku_tarih_ve_saat.month)+str(bugunku_tarih_ve_saat.year)+str(a+1)

    return b
def success(request):
    context = dict()
    if request.user.is_authenticated:
        ads =  sepet_sahibi_bilgileri.objects.filter(kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last()).last()
        user_sepet = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last()
        satin_alinanlar.objects.create(siparis_numarasi = bugunsiparis()+"IHavale"+str(user_sepet.id),siparis_sahibi_bilgileri = ads,kayitli_kullanici = user_sepet,)
        sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).update(sepet_satin_alma_durumu = True)
        a = sepetteki_urunler.objects.filter(kayitli_kullanici = user_sepet)
        toplam_fiyat = 0
        for i in a:
            isilem = get_object_or_404(urun,id = i.urun_bilgisi.id).urun_stok-i.urun_adedi
            urun.objects.filter(id = i.urun_bilgisi.id).update(urun_stok = isilem)
    else:
        ads = get_object_or_404(sepet_sahibi_bilgileri,kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last())
        user_sepet = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last()
        satin_alinanlar.objects.create(siparis_numarasi = bugunsiparis()+"KHavale"+str(user_sepet.id),siparis_sahibi_bilgileri = ads,kayitli_olmayan_kullanici = user_sepet,)
        sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).update(sepet_satin_alma_durumu = True)
        a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = user_sepet)
        toplam_fiyat = 0
        for i in a:
            isilem = get_object_or_404(urun,id = i.urun_bilgisi.id).urun_stok-i.urun_adedi
            urun.objects.filter(id = i.urun_bilgisi.id).update(urun_stok = isilem)

    return redirect("/")