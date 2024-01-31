from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render,get_object_or_404
from .models import *
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from main.views import site_bilgileri
# Create your views here.
@user_not_authenticated
def register(request):
    context = site_bilgileri()
    form = RegisterForm(request.POST or None)
    context["form"] = form

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email_address = form.cleaned_data.get("email_address")
        newUser = CustomUser(username =username,email = email_address)
        newUser.set_password(password)

        newUser.save()
        login(request,newUser)
        messages.info(request,"Başarıyla Kayıt Oldunuz...")

        return redirect("/")
    
    return render(request,"account/register.html",context)


@user_not_authenticated
def loginUser(request):
    context = site_bilgileri()
    form = LoginForm(request.POST or None)


    context["form"] = form

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)

        messages.success(request,"Başarıyla Giriş Yaptınız")
        login(request,user)
        return redirect("/")
    return render(request,"account/login.html",context)
@login_required
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("/")

def login_yaptir(request):
    if request.POST:
        emailkullaniciadi = request.POST.get("emailkullaniciadi")
        sifresi = request.POST.get("sifresi")
        user = authenticate(username = emailkullaniciadi,password = sifresi)
        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return redirect("/users/login/")
        login(request,user)
        return redirect("/")
    

def kayit_ol(request):
    if request.POST:
        emailkullaniciadi = request.POST.get("emailkullaniciadi")
        sifresi = request.POST.get("sifresi")
        newUser = CustomUser(username =emailkullaniciadi,email = emailkullaniciadi)
        newUser.set_password(sifresi)

        newUser.save()
        login(request,newUser)
        return redirect("/")