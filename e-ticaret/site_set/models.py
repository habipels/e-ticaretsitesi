from django.db import models
# Create your models here.
# Create your models here.
from PIL import Image
from io import BytesIO
class sayfa_logosu(models.Model):
    image  = models.ImageField(upload_to='logo/',verbose_name="Sayfaya Logo Ekleyin")
    def save(self, *args, **kwargs):
        super(sayfa_logosu, self).save(*args, **kwargs)
        if self.image:
            with Image.open(self.image.path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                width, height = img.size
                if width > 800:
                    new_width = 800
                    new_height = int((new_width / width) * height)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=60)
                    self.image.save(self.image.name, content=buffer, save=False)
                    super(sayfa_logosu, self).save(*args, **kwargs)
class sayfa_iconu(models.Model):
    sayfa_icon = models.FileField(upload_to='logo/',verbose_name="Sayfaya ikon ekleyin")
class site_adi(models.Model):
    site_adi_genel = models.CharField(max_length=200,verbose_name="Google Nasıl Görünecek")
    site_adi_sekme_tr= models.CharField(max_length=200,verbose_name="Sekmede Görünme Türkçe")
    def __str__(self):
        return self.site_adi_genel


class numara(models.Model):
    sirket_numarasi_gosterilecek_metin = models.CharField(max_length=20,verbose_name="Telefon Sitede Nasıl görünecek" )
    sirket_numarasi = models.CharField(max_length=20,verbose_name="Aranacak Numara Başında + olmadan ülke kodu ile Yazabilirisniz")
    def __str__(self):
        return self.sirket_numarasi_gosterilecek_metin

class adres(models.Model):
    sirket_adresi_tr = models.CharField(max_length=200,verbose_name="Şirket Adresi Türkçe")
    def __str__(self):
        return self.sirket_adresi_tr
class gomulu_adres(models.Model):
    sirket_adresi_tr = models.CharField(max_length=1000,verbose_name="Şirket Adresi Türkçe")
    def __str__(self):
        return self.sirket_adresi_tr
class email_adres(models.Model):
    sirket_email_adresi = models.EmailField(max_length=200,verbose_name="Şirket Email Adresi")
    def __str__(self):
        return self.sirket_email_adresi

class sosyalmedyaInsgr(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket İnstagram Linki")

class sosyalmedyalinkd(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket Linkedin Linki")
class sosyalmedyaFace(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket Facebook Linki")
class sosyalmedyayoutube(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket Youtube Linki")
class sosyalmedyatw(models.Model):
    link = models.CharField(max_length=400,verbose_name="Şirket TW Linki")
class seo_ayarlari(models.Model):
    site_seo_kelimeleri_tr =models.TextField(max_length=400,verbose_name="Seo Kelmeleri Türkçe")
    site_seo_metni_tr = models.TextField(max_length=400,verbose_name="Seo Metni Türkçe")

class banner(models.Model):
    banner_basligi_tr =models.CharField(max_length=400,verbose_name="Banner Başliği Türkçe")
    banner_aciklama_tr = models.TextField(max_length=400,verbose_name="Banner Aciklama Türkçe")
    banner_sira = models.IntegerField(verbose_name="Banner Gösterme Sırası")
    banner_gosterme = models.BooleanField(verbose_name="Banner Gösterilsin mi ? ")
    banner_link = models.CharField(max_length=400,verbose_name="Bannera Link Brakmak İstiyorsanız link Ekleyin",null=True,blank=True)
    image  = models.ImageField(upload_to='banner/',blank = True,null = True,verbose_name="Sayfaya Banner Ekleyin")
    def save(self, *args, **kwargs):
        super(banner, self).save(*args, **kwargs)
        if self.image:
            with Image.open(self.image.path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                width, height = img.size
                if width > 800:
                    new_width = 800
                    new_height = int((new_width / width) * height)
                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=60)
                    self.image.save(self.image.name, content=buffer, save=False)
                    super(banner, self).save(*args, **kwargs)


from ckeditor.fields import RichTextField
class hakkimizda(models.Model):
    hakkimizda_tr = RichTextField(verbose_name="Hakkımızda Yazısı Türkçe")
    
class anasayfa(models.Model):
    
    hakkimizda_tr = RichTextField(verbose_name="Anasayfa Yazısı Türkçe")
class odeme_ayarlari_paytr(models.Model):
    magaza_adi = models.CharField(max_length = 200,verbose_name = "Mağaza Adı")
    magaza_parolasi = models.CharField(max_length = 400,verbose_name = "Mağaza Parolası")
    magaza_gizli_anahtar = models.CharField(max_length = 400,verbose_name = "Mağaza Gizli Anahtar")

class yasal_metinler(models.Model):
    yasal_metin_basligi = models.CharField(max_length = 200,verbose_name = "yasal Metin Başlığı")
    yasalmetin = RichTextField(verbose_name="Yasal Metin İçeriği")

class kargo_tutari(models.Model):
    min_siparis_tutari = models.FloatField(default = 0)
    eklenecek_kargo_tutari = models.FloatField(default = 0)

class sitefooteryazisiz(models.Model):
    site_footer_yazisi = models.CharField(max_length=400,verbose_name="site Footer Yazısı")