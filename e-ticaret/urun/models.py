from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class kategory_link_ayari(models.CharField):
    def __init__(self, *args, **kwargs):
        super(kategory_link_ayari, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return str(value).lower().replace(" ","_")
    

class user_adi(models.CharField):
    def __init__(self, *args, **kwargs):
        super(user_adi, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return str(value).upper()
class Meslek(models.Model):
    kategori= user_adi(verbose_name="Kategori Adı Türkçe",max_length=100)
    ust_kategory = models.ForeignKey('self',blank=True,null=True,verbose_name="Üst Kategori Bilgisi",related_name='children',on_delete=models.CASCADE)
    link = kategory_link_ayari(max_length=200)
    keywords = models.CharField(max_length=255)
    silinme_bilgisi = models.BooleanField(default=False,verbose_name="Silinme Bilgisi")
    def __str__(self):
        full_path = [self.kategori]                  # post.  use __unicode__ in place of
        k = self.ust_kategory
        while k is not None:
            full_path.append(k.kategori)
            k = k.ust_kategory
        return ' --> '.join(full_path[::-1])
    
class filtre(models.Model):
    filtre_adi= user_adi(verbose_name="Filtre Adı Türkçe",max_length=100)
    filtre_bagli_oldu_kategori = models.ForeignKey(Meslek,blank=True,null=True,verbose_name=" Kategori Bilgisi",on_delete=models.SET_NULL)
    silinme_bilgisi = models.BooleanField(default=False,verbose_name="Silinme Bilgisi")
    filtre_linki = kategory_link_ayari(max_length=200,verbose_name="Filtre Linki",blank=True,null=True)
    def __str__(self):
        full_path = [self.filtre_adi]                  
        return ' --> '.join(full_path[::-1])

class filtre_icerigi(models.Model):
    filtre_adi= user_adi(verbose_name="Filtre Adı Türkçe",max_length=100)
    filtre_bagli_oldu_filtre = models.ForeignKey(filtre,blank=True,null=True,verbose_name=" Kategori Bilgisi",on_delete=models.SET_NULL)
    silinme_bilgisi = models.BooleanField(default=False,verbose_name="Silinme Bilgisi")
    filtre_renk_kodu = models.CharField(max_length=200,verbose_name="Renk Eklemek ilsterseniz",blank=True,null=True)
    
    def __str__(self):
        full_path = [self.filtre_adi]                  
        return ' --> '.join(full_path[::-1])
    

class urun(models.Model):
    kategori = models.ManyToManyField(Meslek,blank=True,null=True)
    urun_adi  = models.CharField(max_length=200,verbose_name="Ürün Adı",blank=True,null=True)
    fiyat = models.FloatField(verbose_name="Fiyat Bilgisi", blank=True,null=True)
    urun_stok = models.FloatField(blank=True,null=True,verbose_name="Stok Bilgisi")
    urun_aciklama = RichTextField(verbose_name="Ürün Açıklama")
    silinme_bilgisi = models.BooleanField(default=False,verbose_name="Silinme Bilgisi")
    urun_bakma_saysi = models.BigIntegerField(verbose_name="Ürün Bakma Sayısı" ,default=0)
from PIL import Image
from io import BytesIO
class urun_resimleri(models.Model):
    urun_bilgisi = models.ForeignKey(urun,blank=True,null=True,verbose_name="Ürün Bilgisi", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    

class urun_filtre_tercihi(models.Model):
    urun = models.ForeignKey(urun,verbose_name="Ürün Bilgisi",blank=True,null=True,on_delete=models.CASCADE)
    filtre_bilgisi =  models.ForeignKey(filtre_icerigi,verbose_name="Filtre İçeriğini Seç",blank=True,null=True,on_delete=models.SET_NULL)
    