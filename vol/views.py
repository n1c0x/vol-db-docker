from django.shortcuts import render,get_object_or_404
from django_tables2 import RequestConfig

from .models import Vol
from .tables import VolTable

# Create your views here.

def index(request):
    vols_list = Vol.objects.order_by('-date')[:5]
    context = {
        'vols_list': vols_list
    }
    return render(request, 'vol/index.html', context)

def detail(request,vol_id):
    vol = get_object_or_404(Vol, pk=vol_id)
    return render(request, 'vol/detail.html', {'vol': vol})