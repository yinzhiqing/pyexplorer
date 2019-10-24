from django.urls import path

from . import views

app_name = 'proof'
urlpatterns = [
  path('btctx/', views.btctx, name='btctx'),
  path('<str:name>/btcproof/', views.btcproof, name='btcproof'),
  path('btcnames/', views.btcnames, name='btcnames'),
]

