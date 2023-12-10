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