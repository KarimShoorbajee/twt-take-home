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
    #VehicleModel.objects.all().delete()
    #Country.objects.all().delete()
    #Make.objects.all().delete()
    
    make_dict = {}
    country_dict = {}
    model_dict = {}

    URL =  "https://my.api.mockaroo.com/karim.json?key=e6ac1da0"
    get_req = requests.get(url = URL)
    data = get_req.json()

    for x in data:
        if ("make" in x):
            if x["make"] not in make_dict:
                m = Make(name = x["make"])
                m.save()
                make_dict[x["make"]]= m.pk
            else:
                m = Make.objects.get(pk=make_dict[x["make"]])
        if ("model" in x):
            if x["model"] not in model_dict:
                vm = VehicleModel(name = x["model"], model_make = m)
                vm.save()
                model_dict[x["model"]]= vm.pk
            else:
                vm = VehicleModel.objects.get(pk=model_dict[x["model"]])
        if x["import_country"] not in country_dict:
            c = Country(name = x["import_country"], total_sales = x["sale_price"])
            c.save()
            country_dict[x["import_country"]] = c.pk
        else:
            c = Country.objects.get(pk = country_dict[x["import_country"]])
            c.total_sales += x["sale_price"]
        
        new_sale = Sale(country = c, sale_model = vm, sale_price = x["sale_price"])
        new_sale.save()

    return HttpResponse("AHHHHHHH")

