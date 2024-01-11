from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404

import json

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
import pprint
from .models import *

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



import base64
import hashlib
import hmac
import html
import json
import random

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from site_set.models import *
from urun.models import *
def home(request):
    content = dict()
    merchant_id = odeme_ayarlari_paytr.objects.last().magaza_adi
    merchant_key = bytes(odeme_ayarlari_paytr.objects.last().magaza_parolasi, 'utf-8')
    merchant_salt = bytes(odeme_ayarlari_paytr.objects.last().magaza_gizli_anahtar, 'utf-8')
    merchant_ok_url = "http://127.0.0.1:8000/pay/success/"
    merchant_fail_url = 'http://127.0.0.1:8000/pay/result?basari=NO'
    context = dict()
    if request.user.is_authenticated:
        ads =  get_object_or_404(sepet_sahibi_bilgileri,kayitli_kullanici = sepet_olusturma.objects.filter(sepet_sahibi = request.user).last())
        user_sepet = sepet_olusturma.objects.filter(sepet_sahibi = request.user,sepet_satin_alma_durumu = False).last()
        sepetteki_urunler_getir = []
        a = sepetteki_urunler.objects.filter(kayitli_kullanici = user_sepet)
        toplam_fiyat = 0
        for i in a:
            sepetteki_urunler_getir.append([str(i.urun_bilgisi.urun_adi),str(i.urun_bilgisi.fiyat),int(i.urun_adedi)])
            toplam_fiyat = toplam_fiyat+ (float(i.urun_bilgisi.fiyat)*int(i.urun_adedi))
    else:
        ads = get_object_or_404(sepet_sahibi_bilgileri,kayitli_olmayan_kullanici = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last())
        user_sepet = sepet_olusturma_ip.objects.filter(sepet_sahibi = get_client_ip(request),sepet_satin_alma_durumu = False).last()
        sepetteki_urunler_getir = []
        a = sepetteki_urunler.objects.filter(kayitli_olmayan_kullanici = user_sepet)
        toplam_fiyat = 0
        for i in a:
            sepetteki_urunler_getir.append([str(i.urun_bilgisi.urun_adi),str(i.urun_bilgisi.fiyat),int(i.urun_adedi)])
            toplam_fiyat = toplam_fiyat+ (float(i.urun_bilgisi.fiyat)*int(i.urun_adedi))
    print(sepetteki_urunler_getir)
    user_basket = base64.b64encode(json.dumps(sepetteki_urunler_getir).encode())

    merchant_oid ='OS' + random.randint(1, 9999999).__str__()+"ID"+ str(user_sepet.id)
    test_mode = '1'
    debug_on = '1'

    # 3d'siz işlem
    non_3d = '0'

    # Ödeme süreci dil seçeneği tr veya en
    client_lang = "tr"

    # non3d işlemde, başarısız işlemi test etmek için 1 gönderilir (test_mode ve non_3d değerleri 1 ise dikkate alınır!)
    non3d_test_failed = '0'
    user_ip = str(get_client_ip(request))
    email = str(ads.email)

    # 100.99 TL ödeme
    payment_amount = str(int(toplam_fiyat)*100)
    currency = 'TL'
    payment_type = 'card'
    user_name = str(ads.isim)+" "+ str(ads.soyisim)
    user_address = str(ads.adres) + " "+str(ads.sehirler)+" "+str(ads.ulke)
    user_phone = str(ads.telefon)
    no_installment = "1"
    max_installment="3"
    # Alabileceği değerler; advantage, axess, combo, bonus, cardfinans, maximum, paraf, world, saglamkart
    card_type = 'bonus'
    installment_count = '1'

    hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + user_basket.decode()+ no_installment + max_installment + currency + test_mode
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())
    context = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_type': payment_type,
        'payment_amount': payment_amount,
        'currency': currency,
        'test_mode': test_mode,
        'non_3d': non_3d,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'user_basket': user_basket.decode(),
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'client_lang': client_lang,
        'paytr_token': paytr_token.decode(),
        'non3d_test_failed': non3d_test_failed,
        'installment_count': installment_count,
        'card_type': card_type,

    }
    result = requests.post('https://www.paytr.com/odeme/api/get-token', context)
    res = json.loads(result.text)

    if res['status'] == 'success':
        print(res['token'])
        print(result.text)


        content = {
            'token': res['token']
        }

    else:
        print(result.text)
    return render(request, 'odeme/payment.html', res)

@csrf_exempt
def callback(request):

    #return redirect("/")

    if request.method != 'post':
        return HttpResponse(str(request.GET))

    post = request.POST

    # API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
    merchant_id = odeme_ayarlari_paytr.objects.last().magaza_adi
    merchant_key = bytes(odeme_ayarlari_paytr.objects.last().magaza_parolasi, 'utf-8')
    merchant_salt = bytes(odeme_ayarlari_paytr.objects.last().magaza_gizli_anahtar, 'utf-8')

    # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    # POST değerleri ile hash oluştur.
    hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
    hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())

    # Oluşturulan hash'i, paytr'dan gelen post içindeki hash ile karşılaştır
    # (isteğin paytr'dan geldiğine ve değişmediğine emin olmak için)
    # Bu işlemi yapmazsanız maddi zarara uğramanız olasıdır.
    if hash != post['hash']:
        return HttpResponse(str('PAYTR notification failed: bad hash'))

    # BURADA YAPILMASI GEREKENLER
    # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
    # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.

    if post['status'] == 'success':  # Ödeme Onaylandı
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi onaylayın.
        2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
        3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir.
        Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
        """
        print(request)

    else:  # Ödemeye Onay Verilmedi
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi iptal edin.
        2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
        post['failed_reason_code'] - başarısız hata kodu
        post['failed_reason_msg'] - başarısız hata mesajı
        """
        print(request)

    # Bildirimin alındığını PayTR sistemine bildir.
    return HttpResponse(str('OK'))


def success(request):
    context = dict()
    messages.success(request, f"Paket Satın Alma Başarılı")
    return redirect("/")


def fail(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'

    messages.success(request, f"Bundle Purchase Failed")
    return HttpResponse("Bundle Purchase Failed")