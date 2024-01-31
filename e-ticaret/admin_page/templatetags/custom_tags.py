from django import template
from urun.models import *
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from site_set.models import *
register = template.Library()

@register.filter
def Filtre_icerikleri_alma(stok_kart):
    
    satis_fiyati = filtre_icerigi.objects.filter(filtre_bagli_oldu_filtre=stok_kart.id)
    icerikler = ""
    #
    for i in satis_fiyati:
        icerikler = icerikler+'<button  type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#logogeldi{}"">{}</button>'.format(i.id,i.filtre_adi)
    return mark_safe(icerikler)

@register.filter
def filtre_silmek_icin(stok_kart):
    satis_fiyati = filtre_icerigi.objects.filter(filtre_bagli_oldu_filtre=stok_kart.id)
    icerikler =""
    a = """<div class="modal" id="logogeldi{}">
  <div class="modal-dialog">
    <div class="modal-content">

      <!-- Modal Header -->
      <div class="modal-header">
        <h4 class="modal-title">İçeriği Sil</h4>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>

      <!-- Modal body -->
      <div class="modal-body" style="height: 100px;">

            Bu {} Filtre İçeriğini Silmek İstediğinden Emin misin ? 
            
            

      </div>

      

      <!-- Modal footer -->
      <div class="modal-footer">
        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">iptal</button>
            <a href="/yonetim/filtreicerigisil/{}"  class="btn btn-success" >sil</a>    
    </div></div>

    </div>
  </div>
</div>"""
    #
    for i in satis_fiyati:
        icerikler = icerikler+a.format(i.id,str(i.filtre_adi),i.id)
    return mark_safe(icerikler)
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
    
    satis_fiyati = urun_filtre_tercihi.objects.filter(urun=stok_kart)
    icerikler = ""
    for i in satis_fiyati:
        icerikler = icerikler+","+str(i.filtre_bilgisi)+"\n"
        
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
    try:
        veri_bir = urun_filtre_tercihi.objects.filter(urun = stok_kart.id )
        veri_gonder = ""
        for z in veri_bir:
            veri_gonder = veri_gonder+class_yapisi+str(z.filtre_bilgisi.filtre_bagli_oldu_filtre.filtre_adi)+": </p><span>"+str(z.filtre_bilgisi.filtre_adi)+"</span>"+class_yapisi_devam
    except:
        pass
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
    a = kargo_tutari.objects.last()
    if toplam_tutar > a.min_siparis_tutari:
        toplam_tutar = "Size Ait".format(a.eklenecek_kargo_tutari)
    else:
        toplam_tutar = "Size Ait".format(a.eklenecek_kargo_tutari)
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
    a = kargo_tutari.objects.last()
    if toplam_tutar > a.min_siparis_tutari:
        toplam_tutar = toplam_tutar
    else:
        toplam_tutar = toplam_tutar 
    return round(float(toplam_tutar), 2)
@register.simple_tag
def kategoi_bilgisi_duzednleme(id):
    veri = ''
    if id == "":
        a = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = None,headerda_gosterme = True).order_by("numarasi")
        y = 0
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id).order_by("numarasi")
            if z.count() > 0:
                veri = veri+ '<li class="step1"><a href="/kategori/{}/{}/"> <i class="fas fa fa-sort-down">  </i> {}</a><div class="open"><div class="left_con"><ul class="">'.format(str(i.id),str(i.link),str(i.kategori))
                k = 0
                for j in z:
                    veri = veri+str(kategoi_bilgisi_duzednleme(j.id))
                    k = k+1
                    if k >=5:
                        veri = veri+ '<li class="step1"><a style="color: var(--orange);font-size: small;" href="/kategori/{}/{}/">Tümünü Gör</a></li>'.format(str(i.id),str(i.link))
                        break
                veri = veri + '</ul></div></div></li>'
            else:
                veri = veri+ '<li class="step1"><a href="/kategori/{}/{}/">{}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
            y = y+1
            if y >= 5:
                break
    else:
        a = Meslek.objects.filter(silinme_bilgisi = False,id = id).order_by("numarasi")   
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id).order_by("numarasi")
            if z.count() > 0:
                veri = veri+ '<li> <a href="/kategori/{}/{}/"><i class="fas fa fa-sort-down"> </i> {}</a> <div class="left_con"><ul class="open2">'.format(str(i.id),str(i.link),str(i.kategori))
                for j in z:
                    veri = veri+'{}'.format(str(kategoi_bilgisi_duzednleme(j.id)))
                veri = veri + "</ul></li></div>"
            else:
                veri = veri+ '<li class=""><a class="" href="/kategori/{}/{}/"><i class="fas fa-angle-right"></i> {}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
    return  mark_safe(veri)
@register.simple_tag
def kategoi_bilgisi_duzednleme2(id):
    
    veri = ''
    if id == "":
        a = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = None,headerda_gosterme = True).order_by("numarasi")
        y = 0
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id).order_by("numarasi")
            
            if z.count() > 0:
                veri = veri+'<li><a href="/kategori/{}/{}/"" title="{}">{}</a><div class="sub1"><div class="wrap"><div class="left"><ul>'.format(str(i.id),str(i.link),str(i.kategori),str(i.kategori))
                k = 0
                for j in z:
                    veri = veri+str(kategoi_bilgisi_duzednleme(j.id))
                    k = k+1
                    if k >=5:
                        veri = veri+ '<li class="step1"><a style="color: var(--orange);font-size: small;" href="/kategori/{}/{}/">Tümünü Gör</a></li>'.format(str(i.id),str(i.link))
                        break
                veri = veri + '</ul></div></div></div></li>'
            else:
                veri = veri+ '<li class=""><a class="" href="/kategori/{}/{}/">{}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
    else:
        a = Meslek.objects.filter(silinme_bilgisi = False,id = id).order_by("numarasi")   
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id).order_by("numarasi")
            
            if z.count() > 0:
                veri = veri+ '<li> <a href="/kategori/{}/{}/"><i class="fas fa fa-sort-down"> </i> {}</a> <div class="left_con"><ul class="open2">'.format(str(i.id),str(i.link),str(i.kategori))
                for j in z:
                    veri = veri+'{}'.format(str(kategoi_bilgisi_duzednleme(j.id)))
                    
                veri = veri + "</ul></li></div>"
            else:
                veri = veri+ '<li class=""><a class="" href="/kategori/{}/{}/"><i class="fas fa-angle-right"></i> {}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
            y = y+1
            if y >= 5:
                break
    return  mark_safe(veri)
@register.simple_tag
def getir(id):
    b = ""
    z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = id).order_by("numarasi")
    y = 0
    for i in z:
        b = b+'<li><a href="/kategori/{}/{}/"><i class="fas fa-angle-right"></i>{}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
        y = y+1
        if y >= 5:
            b = b+'<li><a href="/kategori/{}/{}/" style="color: var(--orange);font-size: small;">Tümünü Gör</a></li>'.format(str(i.ust_kategory.id),str(i.ust_kategory.link))
            break
    return b
@register.simple_tag
def tumkategoriler(bilgi):
    a = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = None).order_by("numarasi")
    bilgi = ""
    for i in a:
        bilgi = bilgi+'<li> <a href="/kategori/{}/{}/">{}</a><ul class="open2">'.format(str(i.id),str(i.link),str(i.kategori))
        bilgi = bilgi+getir(i.id)+'</ul></li>'
    return mark_safe(bilgi)

@register.simple_tag
def sepet_id_gonder(a):
    for i in a:
        if i.kayitli_kullanici:
            return  "kayitli"+str(i.kayitli_kullanici.id)
        else:
            return "ip"+str(i.kayitli_olmayan_kullanici.id)
        

@register.simple_tag
def urun_gosterecek_kayitli(bilgi):
    a = sepetteki_urunler.objects.filter(kayitli_kullanici_id  = bilgi)
    b = ""
    for i in a:
        if i.urun_adedi > 0:
            isi = "/urun/{}/{}".format(i.urun_bilgisi.id,str(i.urun_bilgisi.urun_adi).replace("/","_").replace(" ","_"))
            b = b+ '<a href="{}" target="_blank" rel="noopener noreferrer">Adet :{} - Ürün : {}</a> <br>'.format(isi,i.urun_adedi,i.urun_bilgisi.urun_adi)
    return mark_safe(b)

@register.simple_tag
def urun_gosterecek_kayitli_bilgi(bilgi):
    a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici_id  = bilgi)
    b = ""
    for i in a:
        if i.urun_adedi > 0:
            isi = "/urun/{}/{}".format(i.urun_bilgisi.id,str(i.urun_bilgisi.urun_adi).replace("/","_").replace(" ","_"))
            b = b+ '<a href="{}" target="_blank" rel="noopener noreferrer">Adet : {} - Ürün : {}</a> <br>'.format(isi,i.urun_adedi,i.urun_bilgisi.urun_adi)
    return mark_safe(b)

@register.simple_tag
def kullanici_sayisi():
    a =CustomUser.objects.all().count()
    return a
@register.simple_tag
def urun_sayisi():
    a =urun.objects.all().count()
    return a
@register.simple_tag
def alinansiparisler():
    a =satin_alinanlar.objects.all().count()
    return a

@register.simple_tag
def bugunsiparis():
    bugunku_tarih_ve_saat = datetime.now()
    a =satin_alinanlar.objects.filter(kayit_tarihi__gte=bugunku_tarih_ve_saat.replace(hour=0, minute=0, second=0, microsecond=0)).count()
    return a
@register.simple_tag
def bugunsiparistutar():
    bugunku_tarih_ve_saat = datetime.now()
    a =satin_alinanlar.objects.filter(kayit_tarihi__gte=bugunku_tarih_ve_saat.replace(hour=0, minute=0, second=0, microsecond=0))
    toplam = 0
    for i in a:
        if i.siparis_sahibi_bilgileri.kayitli_kullanici:
            k =sepetteki_urunler.objects.filter(kayitli_kullanici =i.siparis_sahibi_bilgileri.kayitli_kullanici )
            for j in k:
                toplam = toplam+(j.urun_adedi* j.urun_bilgisi.fiyat)
        else:
            k =sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici =i.siparis_sahibi_bilgileri.kayitli_olmayan_kullanici )
            for j in k:
                toplam = toplam+(j.urun_adedi* j.urun_bilgisi.fiyat)
    return str(toplam)
from datetime import datetime, timedelta
@register.simple_tag
def ayliksiparistutar():
    bugunku_tarih_ve_saat = datetime.now()
    ay_baslangici = bugunku_tarih_ve_saat.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    aylar_ara = ay_baslangici - timedelta(days=1)
    aylar_ara = aylar_ara.replace(day=1)

    a = satin_alinanlar.objects.filter(kayit_tarihi__gte=aylar_ara, kayit_tarihi__lte=bugunku_tarih_ve_saat)
    toplam = 0
    
    for i in a:
        if i.siparis_sahibi_bilgileri.kayitli_kullanici:
            k = sepetteki_urunler.objects.filter(kayitli_kullanici=i.siparis_sahibi_bilgileri.kayitli_kullanici)
            for j in k:
                toplam = toplam + (j.urun_adedi * j.urun_bilgisi.fiyat)
        else:
            k = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici=i.siparis_sahibi_bilgileri.kayitli_olmayan_kullanici)
            for j in k:
                toplam = toplam + (j.urun_adedi * j.urun_bilgisi.fiyat)

    return str(toplam)
@register.simple_tag
def yilliksiparistutar():
    bugunku_tarih_ve_saat = datetime.now()
    yil_baslangici = bugunku_tarih_ve_saat.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    aylar_ara = yil_baslangici - timedelta(days=1)
    aylar_ara = aylar_ara.replace(month=1, day=1)

    a = satin_alinanlar.objects.filter(kayit_tarihi__gte=aylar_ara, kayit_tarihi__lte=bugunku_tarih_ve_saat)
    toplam = 0
    
    for i in a:
        if i.siparis_sahibi_bilgileri.kayitli_kullanici:
            k = sepetteki_urunler.objects.filter(kayitli_kullanici=i.siparis_sahibi_bilgileri.kayitli_kullanici)
            for j in k:
                toplam = toplam + (j.urun_adedi * j.urun_bilgisi.fiyat)
        else:
            k = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici=i.siparis_sahibi_bilgileri.kayitli_olmayan_kullanici)
            for j in k:
                toplam = toplam + (j.urun_adedi * j.urun_bilgisi.fiyat)

    return str(toplam)

@register.simple_tag
def duzenle(a):
    return a.replace("/","-").replace(" ","_")
@register.simple_tag
def indirim_orani(a,b):
    return 100 - int(b*100/a)


@register.simple_tag
def benzer_urunler(id):
    a = get_object_or_404(Meslek,id = id)
    tum_kategoriler = []
    for i in Meslek.objects.filter(silinme_bilgisi = False):
        if a.kategori in i.__str__() :
            tum_kategoriler.append(i.id)
    profile1 = urun.objects.filter(urun_stok__gte=1,kategori__id__in = tum_kategoriler,silinme_bilgisi = False).distinct()[0:4]
    profile2 = urun.objects.filter(urun_stok__gte=1,kategori__id__in = tum_kategoriler,silinme_bilgisi = False).distinct()[4:8]
    profile3 = urun.objects.filter(urun_stok__gte=1,kategori__id__in = tum_kategoriler,silinme_bilgisi = False).distinct()[8:12]
    profile={
        "profile1":profile1,
        "profile2":profile2,
        "profile3":profile3,
    }
    return profile

@register.simple_tag
def kategoimobil(id):
    veri = ''
    if id == "":
        a = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = None).order_by("numarasi")
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id).order_by("numarasi")
            
            if z.count() > 0:
                veri = veri+ '''<li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="/kategori/{}/{}/" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            {}
                        </a>
                        <ul class="dropdown-menu">
                            
                        '''.format(str(i.id),str(i.link),str(i.kategori))
                for j in z:
                    veri = veri+str(kategoimobil(j.id))
                veri = veri + '</ul></li>'
            else:
                veri = veri+ '<li><a class="dropdown-item" href="/kategori/{}/{}/">{}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
    else:
        a = Meslek.objects.filter(silinme_bilgisi = False,id = id).order_by("numarasi")   
        for i  in a:
            z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = i.id).order_by("numarasi")
            
            if z.count() > 0:
                veri = veri+'''<li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="/kategori/{}/{}/" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            {}
                        </a>
                        <ul class="dropdown-menu">
                            
                        '''.format(str(i.id),str(i.link),str(i.kategori))
                for j in z:
                    veri = veri+'{}'.format(str(kategoimobil(j.id)))
                veri = veri + "</ul></li>"
            else:
                veri = veri+ '<li><a class="dropdown-item" href="/kategori/{}/{}/">{}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
    return  mark_safe(veri)

@register.simple_tag
def getir_kategorileri(id):
    b = ""
    z = Meslek.objects.filter(silinme_bilgisi = False,ust_kategory_id = id).order_by("numarasi")
    y = 0
    for i in z:
        b = b+'<li ><a style="color: black !important;" href="/kategori/{}/{}/"><i style="color: black !important;" class="fas fa-angle-right"></i>{}</a></li>'.format(str(i.id),str(i.link),str(i.kategori))
    return mark_safe(b)