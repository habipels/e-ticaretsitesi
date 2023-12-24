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
def sepet_toplam_tutar(bilgi):
    return 0


@register.simple_tag
def kategoi_bilgisi_duzednleme(id):
    veri = ''
    if id == "":
        a = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = None)
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id)
            
            if z.count() > 0:
                veri = veri+ '''<div class="nav-item dropdown">
                            <a href="#" class="nav-link" data-toggle="dropdown">{} <i class="fa fa-angle-down float-right mt-1"></i></a>
                            <div class="dropdown-menu position-absolute bg-secondary border-0 rounded-0 w-100 m-0">'''.format(str(i.kategori))
                for j in z:
                    veri = veri+'<a href="" class="dropdown-item">{}</a>'.format(str(kategoi_bilgisi_duzednleme(j.id)))
                veri = veri + '''</div>
                        </div>'''
            else:
                veri = veri+ '<a href="" class="nav-item nav-link">{} </a>'.format(str(i.kategori))
    else:
        a = Meslek.objects.filter(silinme_bilgisi = False,id = id)    
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id)
            
            if z.count() > 0:
                veri = veri+ '''<div class="nav-item dropdown">
                            <a href="#" class="nav-link" data-toggle="dropdown"> {} <i class="fa fa-angle-down float-right mt-1"></i></a>
                            <div class="dropdown-menu position-absolute bg-secondary border-0 rounded-0 w-100 m-0">'''.format(str(i.kategori))
                for j in z:
                    veri = veri+'<a href="" class="dropdown-item">{}</a>'.format(str(kategoi_bilgisi_duzednleme(j.id)))
                veri = veri + '''</div>
                        </div>'''
            else:
                veri = veri+ '<a href="" class="nav-item nav-link">{}</a>'.format(str(i.kategori))
    return  mark_safe(veri)