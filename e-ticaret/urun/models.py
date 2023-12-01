from django.db import models

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
    def __str__(self):
        full_path = [self.filtre_adi]                  
        return ' --> '.join(full_path[::-1])
        