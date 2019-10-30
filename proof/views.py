from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
 
from django.contrib import auth

from django.urls import reverse
import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


# Create your views here.
btc_url = "http://%s:%s@192.168.2.137:9409"
btc_urlname = "btc"
btc_urlpwd= "btc"

def index(request):
    template=loader.get_template('proof/index.html')
    context = {
            "name_list" : "hello world.",
            }
    return HttpResponse(template.render(context, request));  

def btcnames(request):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))

    response = rpc_connection.violas_listbtcproofnames()
    template=loader.get_template('proof/btcnames.html')
    context = {
            "name_list" : response,
            }
    return HttpResponse(template.render(context, request));
def btcproofforname(request, name):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))

    template=loader.get_template('proof/btcproof.html')
    response = rpc_connection.violas_getbtcproofforname(name)
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));
    return render(request, 'proof/btcproof.html', context)
def btcproofforaddress(request, address):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))
    response = rpc_connection.violas_getbtcproofforaddress(addr)
    template=loader.get_template('proof/btcproof.html')
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));
    return render(request, 'proof/btcproof.html', context)

def btcmarks(request):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))

    response = rpc_connection.violas_listbtcmarks()
    template=loader.get_template('proof/btcmarks.html')
    context = {
            "marks" : response,
            }
    return HttpResponse(template.render(context, request));
    #return render(request, 'proof/btcmarks.html', context)

def btctx(request):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))

    response = rpc_connection.violas_listbtcproofforstate('create')
    template=loader.get_template('proof/btctx.html')
    context = {
            "btctx_list" : response,
            }
    return HttpResponse(template.render(context, request));


def violasstates(request, start, end):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))


    if end == 0 :
       height = rpc_connection.violas_getviolasproofcurrentheight()
       end = int(height["height"]);

    if start == 0 :
        if end > 25 :
            start = end - 25;

    if request.method == "POST" :
        start = int(request.POST.get("start"))
        end = int(request.POST.get("end"))

    plist = rpc_connection.violas_getviolasproofforheights(start, end)

    template=loader.get_template('proof/violasstates.html')
    context = {
            "proof_list" : plist,
            "start" : start,
            "end": end,
            }
    return HttpResponse(template.render(context, request));

def violasproofforheight(request, height):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))

    response = rpc_connection.violas_getviolasproofforheight(height)

    template=loader.get_template('proof/violasproof.html')
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));

def violasproofforstate(request, state):
    rpc_connection = AuthServiceProxy(btc_url%(btc_urlname, btc_urlpwd))

    response = rpc_connection.violas_getviolasproofforstate(state)

    template=loader.get_template('proof/violasproof.html')
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));


