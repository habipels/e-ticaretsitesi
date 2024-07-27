from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render,get_object_or_404
from .models import *
from .forms import *
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
        try:
            newUser = CustomUser(username =username,email = email_address)
            newUser.set_password(password)

            newUser.save()
            login(request,newUser)
            messages.info(request,"Başarıyla Kayıt Oldunuz...")
        except:
            return redirect("users/login/")
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
    
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                plaintext = get_template('template_reset_password.txt')
                htmly     = get_template('template_reset_password.html')

                d = {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                }

                subject, from_email, to = 'Password Reset', 'from@example.com', 'to@example.com'
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                email = EmailMultiAlternatives(subject, text_content, from_email,[associated_user.email])
                email.attach_alternative(html_content, "text/html")
                #email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                   pass
                else:
                    messages.error(request, "Se, <b>SERVER PROBLEM</b>")

            return redirect('/')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("/")
