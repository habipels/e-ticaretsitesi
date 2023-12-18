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