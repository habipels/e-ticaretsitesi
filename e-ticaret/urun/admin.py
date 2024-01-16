from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Meslek)
admin.site.register(filtre)
admin.site.register(filtre_icerigi)
admin.site.register(urun)
admin.site.register(urun_resimleri)
admin.site.register(urun_filtre_tercihi)
admin.site.register(sepet_olusturma)
admin.site.register(sepet_olusturma_ip)
admin.site.register(sepetteki_urunler)
admin.site.register(sepet_sahibi_bilgileri)
admin.site.register(satin_alinanlar)
admin.site.register(banka_bilgileri)