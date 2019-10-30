from django.urls import path

from . import views

app_name = 'proof'
urlpatterns = [
  path('', views.index, name='index'),
  path('btctx/', views.btctx, name='btctx'),
  path('btcmarks/', views.btcmarks, name='btcmarks'),
  path('<str:name>/btcproofforname/', views.btcproofforname, name='btcproofforname'),
  path('<str:address>/btcproofforaddress/', views.btcproofforaddress, name='btcproofforaddress'),
  path('btcnames/', views.btcnames, name='btcnames'),
  path('<int:start>/<int:end>/violasstates/', views.violasstates, name='violasstates'),
  path('<int:height>/violasproofforheight/', views.violasproofforheight, name='violasproofforheight'),
  path('<str:state>/violasproofforstate/', views.violasproofforstate, name='violasproofforstate'),
]

