from django.urls import path
from .views import (
   home,callback,success,
   fail
)
app_name = "pay"
urlpatterns = [
    #path('', odeme_olusturma, name='odeme_olusturma'),

    path('payment/', home, name='payment'),
    path('result', callback, name='result'),
    path('success/', success, name='success'),
    path('failure/', fail, name='failure'),
    

]