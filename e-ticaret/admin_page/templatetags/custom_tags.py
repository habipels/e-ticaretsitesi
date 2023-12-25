from django import template
from urun.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
register = template.Library()

@register.filter
def Filtre_icerikleri_alma(stok_kart):
    
    satis_fiyati = filtre_icerigi.objects.filter(filtre_bagli_oldu_filtre=stok_kart.id)
    icerikler = ""
    for i in satis_fiyati:
        icerikler = icerikler+","+i.filtre_adi+"\n"
    return icerikler if icerikler else 0
from django.utils.safestring import mark_safe
@register.filter
def Filtre_icerikleri_almaa(stok_kart):
    
    satis_fiyati = filtre_icerigi.objects.filter(filtre_bagli_oldu_filtre=stok_kart.id)
    icerikler = "<option value='"
    a = icerikler
    z = ""
    listee = []
    for i in satis_fiyati:
        icerikler = a+str(i.id)+"'>"+str(i.filtre_adi)+"</option>"
        z = icerikler+z
    return mark_safe(z)

@register.filter
def urun_filtre_icerigi(stok_kart):
    
    satis_fiyati = urun_filtre_tercihi.objects.filter(urun=stok_kart.id)
    icerikler = ""
    for i in satis_fiyati:
        icerikler = icerikler+","+i.filtre_bilgisi.filtre_adi+"\n"
        
    return icerikler if icerikler else "Filtre Seçilmemiş"

@register.filter
def urun_resimleri_alma(stok_kart):
    
    satis_fiyati = urun_resimleri.objects.filter(urun_bilgisi=stok_kart.id).all()
    icerikler = ""
    for i in satis_fiyati:
        if i.image != None:
            icerikler = i.image.url
            break
        
    return icerikler if icerikler else ""

@register.filter
def urun_filteleri_alma_bilgisi(stok_kart):
    class_yapisi = """
<div class="d-flex mb-3">
                    <p class="text-dark font-weight-medium mb-0 mr-3">
"""
    class_yapisi_devam = """

                    
                </div>
"""
    veri_bir = urun_filtre_tercihi.objects.filter(urun = stok_kart.id )
    veri_gonder = ""
    for z in veri_bir:
        veri_gonder = veri_gonder+class_yapisi+str(z.filtre_bilgisi.filtre_bagli_oldu_filtre.filtre_adi)+": </p><span>"+str(z.filtre_bilgisi.filtre_adi)+"</span>"+class_yapisi_devam
    return mark_safe(veri_gonder)


@register.filter
def sepetteki_urun_sayisi(stok_kart):
    
    satis_fiyati = sepet_olusturma.objects.filter(sepet_sahibi=stok_kart.id,sepet_satin_alma_durumu = False).last()
    a = sepetteki_urunler.objects.filter(kayitli_kullanici = satis_fiyati )
    icerikler = 0
    for i in a:
        icerikler = icerikler + 1 
        
    return icerikler if icerikler else ""

#
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@register.filter
def sepetteki_urun_sayisi_kullan(stok_kart):
    
    satis_fiyati = sepet_olusturma_ip.objects.filter(sepet_sahibi=get_client_ip(stok_kart),sepet_satin_alma_durumu = False).last()
    a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = satis_fiyati )
    icerikler = 0
    for i in a:
        icerikler = icerikler + 1 
        
    return icerikler if icerikler else ""

@register.simple_tag
def carpma(a,b):
    return round(float(a*b), 2)
@register.simple_tag
def sepet_toplam_tutar(request):
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
    toplam_tutar = 0
    for i in veriler:
        toplam_tutar = toplam_tutar+ (i.urun_adedi * i.urun_bilgisi.fiyat)
    return round(float(toplam_tutar), 2)

@register.simple_tag
def sepet_toplam_tutar_k(request):
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
    toplam_tutar = 0
    for i in veriler:
        toplam_tutar = toplam_tutar+ (i.urun_adedi * i.urun_bilgisi.fiyat)
    if toplam_tutar > 350:
        toplam_tutar = "<del>150 TL </del>"
    else:
        toplam_tutar = "150 TL "
    return mark_safe(toplam_tutar)
@register.simple_tag
def sepet_toplam_tutar_t(request):
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
    toplam_tutar = 0
    for i in veriler:
        toplam_tutar = toplam_tutar+ (i.urun_adedi * i.urun_bilgisi.fiyat)
    if toplam_tutar > 350:
        toplam_tutar = toplam_tutar
    else:
        toplam_tutar = toplam_tutar + 350
    return round(float(toplam_tutar), 2)
@register.simple_tag
def kategoi_bilgisi_duzednleme(id):
    veri = ''
    if id == "":
        a = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = None)
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id)
            
            if z.count() > 0:
                veri = veri+ '<li class="allcats"><a class="full_cats" href="/kategori/{}/{}/"> <i class="fas fa fa-sort-down"></i> {}</a><div class="opener"><ul class="open">'.format(str(i.id),str(i.link),str(i.kategori))
                for j in z:
                    veri = veri+str(kategoi_bilgisi_duzednleme(j.id))
                veri = veri + '</ul></div></li>'
            else:
                veri = veri+ '<li class="allcats"><a class="full_cats" href="/kategori/{}/{}/">{}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
    else:
        a = Meslek.objects.filter(silinme_bilgisi = False,id = id)    
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id)
            
            if z.count() > 0:
                veri = veri+ '<li> <a href="/kategori/{}/{}/"><i class="fas fa fa-sort-down"></i> {}</a><ul class="open2">'.format(str(i.id),str(i.link),str(i.kategori))
                for j in z:
                    veri = veri+'{}'.format(str(kategoi_bilgisi_duzednleme(j.id)))
                veri = veri + "</ul></li>"
            else:
                veri = veri+ '<li class="allcats"><a class="full_cats" href="/kategori/{}/{}/"><i class="fas fa fa-sort-down"></i> {}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
    return  mark_safe(veri)