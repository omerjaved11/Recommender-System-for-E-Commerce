from django.shortcuts import render
from django.http import HttpResponse
from  e_commerce.settings import CLIENT_ID,VIEW_ID
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


    #return HttpResponse("<h1>  Subject: "+note.subject+"</h1><h2>Author: "+note.author+ "</h2><h3>Text: "+ note.text +"</h3>")
from django.contrib.auth.decorators import login_required

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def thirdparty(request):
    ctx = {'client_id':CLIENT_ID,'view_id':VIEW_ID,'title':'Dashboard'}
    return render(request,'dashboard/third_party_visualization.html',context=ctx)

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def site_traffic(request):
    ctx = {'client_id':CLIENT_ID,'view_id':VIEW_ID,'title':'Site Traffic'}
    return render(request,'dashboard/site_trafic.html',context=ctx)

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def interactive_chart(request):
    ctx = {'client_id':CLIENT_ID,'view_id':VIEW_ID,'title':'Charts'}
    return render(request,'dashboard/interactive_charts.html',context=ctx)

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def page_view(request):
    ctx = {'client_id':CLIENT_ID,'view_id':VIEW_ID,'title':'Page View'}
    return render(request,'dashboard/page_view.html',context=ctx)

