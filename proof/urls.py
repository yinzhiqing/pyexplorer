from django.urls import path

from . import views

app_name = 'proof'
urlpatterns = [
  path('', views.index, name='index'),
  path('btctx/', views.btctx, name='btctx'),
  path('<str:name>/btcmarks/', views.btcmarks, name='btcmarks'),
  path('<str:name>/btcproofforname/', views.btcproofforname, name='btcproofforname'),
  path('<str:address>/btcproofforaddress/', views.btcproofforaddress, name='btcproofforaddress'),
  path('<str:name>/btcnames/', views.btcnames, name='btcnames'),
  path('<int:start>/<int:end>/<int:height>/violasstates/', views.violasstates, name='violasstates'),
  path('<int:height>/violasproofforheight/', views.violasproofforheight, name='violasproofforheight'),
  path('<str:state>/violasproofforstate/', views.violasproofforstate, name='violasproofforstate'),
  path('<str:state>/<str:address>/<int:sequence>/btcexchange/', views.btcexchange, name='btcexchange'),
]

