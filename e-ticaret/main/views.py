from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from site_set.models import *
from urun.models import *
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.db.models.query_utils import Q
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
    return sozluk
# Create your views here.
def homepage(request):
    content = site_bilgileri()
    profile = urun.objects.filter(urun_stok__gte=1)
    if request.GET.get("search"):
        search = request.GET.get("search")
        profile = urun.objects.filter(Q(urun_adi__icontains = search)  & Q(urun_stok__gte=1) )
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
    return render(request,"index.html",content)

def urunler_tekli_sayfa (request,id,slug):
    content = site_bilgileri()
    content["urun_"] = get_object_or_404(urun,id = id)
    content["urun_resimleri"] = urun_resimleri.objects.filter(urun_bilgisi = get_object_or_404(urun,id = id))
    return render(request,"urunlist/urun_goster.html",content)