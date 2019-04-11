from django.shortcuts import render
from django.http import HttpResponse
from cars.models import Make,Country,VehicleModel,Sale
import requests
import urllib
import json
# Create your views here.

def index(request):
    return HttpResponse("Carrs Index")


'''
Here when we retrieve the car data we clear the databases since this is new data
and we want a clean db
'''
def world(request):
    
    Sale.objects.all().delete()
    Country.objects.all().update(total_sales = 0)

    URL =  "https://my.api.mockaroo.com/karim.json?key=e6ac1da0"
    get_req = requests.get(url = URL)
    data = get_req.json()

    for x in data:
        if ("make" in x):
            make_query = Make.objects.filter(name__iexact = x["make"])
            if not make_query:
                m = Make(name = x["make"])
                m.save()
            else:
                m = make_query[0]
        else: m = None
        if ("model" in x):
            mod_query = VehicleModel.objects.filter(name__iexact = x["model"])
            if not mod_query:
                vm = VehicleModel(name = x["model"])
                if m is not None:
                    vm.model_make = m
                vm.save()
            else:
                vm = mod_query[0]
        else: vm = None
        country_query = Country.objects.filter(name__iexact = x["import_country"])
        if not country_query:
            c = Country(name = x["import_country"], total_sales = x["sale_price"])
            c.save()
        else:
            c = country_query[0]
            c.total_sales += x["sale_price"]
        new_sale = Sale(country = c, sale_model = vm, sale_price = x["sale_price"])
        new_sale.save()

        """
        for mod in VehicleModel.objects.all():
            if not mod.sale_set.all().exists():
                mod.delete()
        """
        for country in Country.objects.all():
            if not country.sale_set.all().exists():
                country.delete()
        '''
        for make in Make.objects.all():
            if not make.vehiclemodel_set.all().exists():
                make.delete()
        '''
    
    return HttpResponse("change it up")

