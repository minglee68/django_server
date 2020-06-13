from django.shortcuts import render
from django.http import HttpResponse

from .models import City

# Create your views here.
def index(request):
    city_list = City.objects.all()
    context = { 'city_list': city_list }
    return render(request, 'basketball/a.html', context)
