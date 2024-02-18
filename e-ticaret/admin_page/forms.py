from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from site_set.models import *
from urun.models import *
class logo_ekle(ModelForm):
    class Meta:
        model = sayfa_logosu
        fields = [
            'image'
        ]

class icon_ekle(ModelForm):
    class Meta:
        model = sayfa_iconu
        fields = [
            'sayfa_icon'
        ]

class Telefon_ekle(ModelForm):
    class Meta:
        model = numara
        fields = [
            'sirket_numarasi_gosterilecek_metin',
            'sirket_numarasi'
        ]


class Email_ekle(ModelForm):
    class Meta:
        model = email_adres
        fields = [
            'sirket_email_adresi'
        ]
class Adress_ekle(ModelForm):
    class Meta:
        model = adres
        fields = [
            'sirket_adresi_tr'
        ]

class insta_ekle(ModelForm):
    class Meta:
        model = sosyalmedyaInsgr
        fields = [
            'link'
        ]
class face_ekle(ModelForm):
    class Meta:
        model = sosyalmedyaFace
        fields = [
            'link'
        ]
class youtube_ekle(ModelForm):
    class Meta:
        model = sosyalmedyayoutube
        fields = [
            'link'
        ]
class linkedin_ekle(ModelForm):
    class Meta:
        model = sosyalmedyalinkd
        fields = [
            'link'
        ]
class tw_ekle(ModelForm):
    class Meta:
        model = sosyalmedyatw
        fields = [
            'link'
        ]

class site_isim_ekle(ModelForm):
    class Meta:
        model = site_adi
        fields = [
            'site_adi_genel',
            'site_adi_sekme_tr',
        ]


class site_seo_ekle(ModelForm):
    class Meta:
        model = seo_ayarlari
        fields = [
            "site_seo_kelimeleri_tr",
            "site_seo_metni_tr",
        ]


class site_banner_ekle(ModelForm):
    class Meta:
        model = banner
        fields = [
            "banner_basligi_tr",
            "banner_aciklama_tr",
            "banner_sira",
            "banner_gosterme",
            "banner_link",
            "image"
        ]

class hakkimizda_ekle(ModelForm):
    class Meta:
        model = hakkimizda
        fields = [
            'hakkimizda_tr',

        ]
class anasayfa_ekle(ModelForm):
    class Meta:
        model = anasayfa
        fields = [
            'hakkimizda_tr',

        ]
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label=" Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class gomuluadres_ekle(ModelForm):
    class Meta:
        model = gomulu_adres
        fields = [
            'sirket_adresi_tr'
        ]

class kategori_ekle(ModelForm):
    kategori = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Kategori Adı','style':'min-width:300px !important; '}),
        label="Kategori Adı")
    link = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Link','style':'min-width:300px !important; '}),
        label="Link")
    keywords = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'keywords','style':'min-width:300px !important; '}),
        label="keywords")
    class Meta:

        model = Meslek
        fields = [
            'kategori',
            'ust_kategory',
            'link',
            'keywords',
            "numarasi",
            "headerda_gosterme"

        ]


class filtre_ekle(ModelForm):
    class Meta:
        model = filtre
        fields = [
            'filtre_adi',
            'filtre_bagli_oldu_kategori'

        ]

class filtre_icerigi_ekle(ModelForm):
    class Meta:
        model = filtre_icerigi
        fields = [
            'filtre_adi'

        ]

class urun_ekle(ModelForm):
    urun_adi = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ürün Adı','style':'min-width:300px !important; '}),
        label="Ürün Adı")
    partikodu = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Parti Kodu','style':'min-width:300px !important; '}),
        label="Parti Kodu")
    class Meta:
        model = urun
        fields = [
            'kategori',
            'urun_adi',
            "partikodu",
            'fiyat',
            'urun_stok',
            "urun_aciklama"

        ]
class yasal_ekle(ModelForm):
    class Meta:
        model = yasal_metinler
        fields = [
            'yasal_metin_basligi',
            'yasalmetin'

        ]
class kargola(ModelForm):
    class Meta:
        model = satin_alinanlar
        fields = [
            'kargo',
            'kargo_sirketi'

        ]
from django import forms



class MultipleImageUploadForm(forms.Form):
    images = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'multiple': True})
    )