from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
 
from django.contrib import auth

from django.urls import reverse
import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from .models import BtcRpc


# Create your views here.
btc_url = "http://%s:%s@%s:%i"
blogin = BtcRpc.objects.order_by('-ip')[:1]
rpc_connection = AuthServiceProxy(btc_url%(blogin[0].user, blogin[0].password, blogin[0].ip, blogin[0].port))
def index(request):
    template=loader.get_template('proof/index.html')
    context = {
            "name_list" : "hello world.",
            }
    return HttpResponse(template.render(context, request));  

def btcnames(request, name):
    response = rpc_connection.violas_listbtcproofnames()
    template=loader.get_template('proof/btcnames.html')
    proof = ""
    if name :
        proof = rpc_connection.violas_getbtcproofforname(name) 
    context = {
            "name_list" : response,
            "proof" : proof
            }
    return HttpResponse(template.render(context, request));
def btcproofforname(request, name):
    template=loader.get_template('proof/btcproof.html')
    response = rpc_connection.violas_getbtcproofforname(name)
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));
    return render(request, 'proof/btcproof.html', context)
def btcproofforaddress(request, address):
    response = rpc_connection.violas_getbtcproofforaddress(addr)
    template=loader.get_template('proof/btcproof.html')
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));
    return render(request, 'proof/btcproof.html', context)

def btcmarks(request, name):
    proof = ""
    amount = 0
    result = {""}
    order = 0;
    message = ""
    response = ""
    template = ""

    try: 
        response = rpc_connection.violas_listbtcmarks()
        template=loader.get_template('proof/btcmarks.html')
        proof = rpc_connection.violas_getbtcproofforname(name)

        if request.method == "POST" :
            result = "inner"
            order = int( request.POST.get("order", 0))
            amount= float( request.POST.get("amount", 0))
            result = rpc_connection.violas_sendbtcproofmark(request.POST.get("fromaddr"), request.POST.get("toaddr"), request.POST.get("vaddr"), int(request.POST.get("order")), request.POST.get("amount"), request.POST.get("name"))
    except:
        message = "exception"
    else:
        message = "successed"
    context = {
            "marks" : response,
            "proof": proof,
            "result": result,
            "fromaddr": request.POST.get("fromaddr", "bitcoin address(hex-string)"),
            "toaddr": request.POST.get("toaddr", 'bitcoin address(hex-string)'),
            "vaddr": request.POST.get("vaddr", 'violas address'),
            "order": order,
            "amount": amount,
            "name": request.POST.get("name", 'proof name(unique)'),
            "message":message
            }
    return HttpResponse(template.render(context, request))

def btctx(request):
    response = rpc_connection.violas_listbtcproofforstate('create')
    template=loader.get_template('proof/btctx.html')
    context = {
            "btctx_list" : response,
            }
    return HttpResponse(template.render(context, request));


def violasstates(request, start, end, height):

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

    proof = ""
    if height >= start and height <= end:
        proof = rpc_connection.violas_getviolasproofforheight(height)
    template=loader.get_template('proof/violasstates.html')
    context = {
            "proof_list" : plist,
            "start" : start,
            "end": end,
            "proof": proof,
            }
    return HttpResponse(template.render(context, request));

def violasproofforheight(request, height):

    response = rpc_connection.violas_getviolasproofforheight(height)

    template=loader.get_template('proof/violasproof.html')
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));

def violasproofforstate(request, state):

    response = rpc_connection.violas_getviolasproofforstate(state)

    template=loader.get_template('proof/violasproof.html')
    context = {
            "proof" : response,
            }
    return HttpResponse(template.render(context, request));

def btcexchange(request, state, address, sequence):
    if state != "start" and state != "end" and state != "cancel":
        state = 'start'
    plist = rpc_connection.violas_listexproofforstate(state)
    proof = ""
    gsequence = 0
    gaddress = ""
    result = ""
    fromaddress = ""
    toaddress = ""
    mod = "start"
    message=""
    amount = 0
    vtoken=""

    if address != '*' or sequence > 0:
        proof = rpc_connection.violas_getexproofforaddress(address, sequence)

    if request.method == "POST" :
        fromaddress = request.POST.get("fromaddress")
        toaddress = request.POST.get("toaddress")
        mod = request.POST.get("mod")
        gaddress = request.POST.get("address")
        gsequence = int(request.POST.get("sequence", 0))
        amount = request.POST.get("amount")
        vtoken = request.POST.get("vtoken")
        if mod == "start":
            result = rpc_connection.violas_sendexproofstart(fromaddress, toaddress, gaddress, gsequence, vtoken)
        elif mod == "end":
            result = rpc_connection.violas_sendexproofend(fromaddress, toaddress, gaddress, gsequence, amount)
        elif mod == "cancel":
            result = rpc_connection.violas_sendexproofcancel(fromaddress, toaddress, gaddress, gsequence)



    template=loader.get_template('proof/btcexchange.html')
    context = {
            "proof" : proof,
            "proof_list": plist,
            "fromaddress": fromaddress,
            "toaddress": toaddress,
            "sequence": gsequence,
            "mod": mod,
            "address": gaddress,
            "amount" : amount,
            "result": result,
            "message": message,
            "vtoken": vtoken,
            "state": state,
            }
    return HttpResponse(template.render(context, request));

