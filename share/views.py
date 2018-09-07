from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


#def index(request):
#    return HttpResponse("Hello,world!")

class HomeView(View):
    def get(self,request):
        return render(request,"base.html",{})
