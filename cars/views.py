from django.shortcuts import render
from django.http import HttpResponse
from cars.models import Make,Country,VehicleModel,Sale
from django.shortcuts import redirect
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

def reset(request,countries=-1):
    if countries == -1:
        URL =  "https://my.api.mockaroo.com/karim.json?key=e6ac1da0"
    else:
        URL = "https://my.api.mockaroo.com/karim.json?key=e6ac1da0&amp;countries=" + countries

    Sale.objects.all().delete()
    VehicleModel.objects.all().delete()
    Make.objects.all().delete()
    Country.objects.all().delete()
    
    make_dict = {}
    country_dict = {}
    model_dict = {}

    get_req = requests.get(url = URL)
    data = get_req.json()

    for x in data:
        if ("make" in x):
            if x["make"] not in make_dict:
                m = Make(name = x["make"], total_sales = x["sale_price"])
                m.save()
                make_dict[x["make"]]= m.pk
            else:
                m = Make.objects.get(pk=make_dict[x["make"]])
                m.total_sales += x["sale_price"]
                m.save()
        else: m = None
        if ("model" in x):
            if x["model"] not in model_dict:
                vm = VehicleModel(name = x["model"], model_make = m, total_sales = x["sale_price"])
                vm.save()
                model_dict[x["model"]]= vm.pk
            else:
                vm = VehicleModel.objects.get(pk=model_dict[x["model"]])
                vm.total_sales += x["sale_price"]
                vm.save()
        else: vm = None
        if x["import_country"] not in country_dict:
            c = Country(name = x["import_country"], total_sales = x["sale_price"])
            c.save()
            country_dict[x["import_country"]] = c.pk
        else:
            c = Country.objects.get(pk = country_dict[x["import_country"]])
            c.total_sales += x["sale_price"]
            c.save()
        
        new_sale = Sale(country = c, sale_model = vm, sale_price = x["sale_price"])
        new_sale.save()

    return redirect('overview')

def overview(request):
    top_countries = []
    top_makes = []
    top_models = []
    for i,x in enumerate(Country.objects.order_by('-total_sales')):
        top_countries.insert(len(top_countries),x)
        if i == 4: break
    for i,x in enumerate(Make.objects.order_by('-total_sales')):
        top_makes.insert(len(top_countries),x)
        if i == 4: break
    for i,x in enumerate(VehicleModel.objects.order_by('-total_sales')):
        top_models.insert(len(top_models),x)
        if i == 4: break
    return render(request, 'cars/overview.html', {'top_countries': top_countries,'top_makes': top_makes,'top_models': top_models,})

def search(request):
    template = 'cars/search.html'
    query = request.GET.get('q')

    country_results = Country.objects.filter(name__icontains=query)
    make_results = Make.objects.filter(name__icontains=query)
    model_results = VehicleModel.objects.filter(name__icontains=query)
    context = {
        'country_results': country_results,
        'make_results': make_results,
        'model_results': model_results,
    }
    return render(request, template, context)

def country(request, pk):
    template = 'cars/country.html'
    country = Country.objects.get(pk=pk)
    country_sales = country.sale_set.all()
    context =  {
        'country': country,
        'sales': country_sales,
    }
    return render(request, template, context)

def make(request, pk):
    template = 'cars/make.html'
    make = Make.objects.get(pk=pk)
    make_models = make.vehiclemodel_set.all()
    make_sales = []
    for model in make_models:
        for sale in model.sale_set.all():
            make_sales.insert(0,sale)
    context =  {
        'make': make,
        'sales': make_sales,
    }
    return render(request, template, context)
    
def model(request, pk):
    template = 'cars/model.html'
    model = VehicleModel.objects.get(pk=pk)
    model_sales = model.sale_set.all()
    context =  {
        'model': model,
        'sales': model_sales,
    }
    return render(request, template, context)