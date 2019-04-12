from django.db import models

# Create your models here.

class Make(models.Model):
    name = models.CharField(max_length=20,blank = True)
    total_sales = models.BigIntegerField(blank=True, default=0)
    def __str__(self):
        return self.name

class Country(models.Model):
    name = name = models.CharField(max_length=100,blank = True)
    total_sales = models.BigIntegerField(blank=True, default=0)
    def __str__(self):
        return "{} {}".format(self.name,self.total_sales)

class VehicleModel(models.Model):
    name = models.CharField(max_length=20,blank = True)
    total_sales = models.BigIntegerField(blank=True, default=0)
    model_make = models.ForeignKey(Make,on_delete=models.CASCADE, null = True)
    def __str__(self):
        return "{} {}".format(self.model_make, self.name)

class Sale(models.Model):
    sale_price = models.IntegerField(blank = True)
    sale_model = models.ForeignKey(VehicleModel,on_delete=models.CASCADE, null= True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE, null = True)
    def __str__(self):
        return " {} {}".format(self.sale_model, self.sale_price)



