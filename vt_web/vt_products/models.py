from django.db import models
from rest_framework_api_key.models import APIKey
from datetime import datetime

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    preview_image = models.ImageField(null=True, blank=True)
    vend_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    datetime = models.DateTimeField(default=datetime.now)
    completed = models.BooleanField(default=False)


class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2) # paid price
    pieces_bought = models.IntegerField()
    pieces_left = models.IntegerField(default=0)
    expiration_date = models.DateField()
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

class Machine(models.Model):
    friendly_name = models.CharField(max_length=255)
    apikey = models.ForeignKey(APIKey, on_delete=models.CASCADE, null=True, blank=True)

class MachineRow(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    chilled = models.BooleanField()

class MachineField(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    max_capacity = models.IntegerField()
    in_stock = models.IntegerField()
    row = models.ForeignKey(MachineRow, on_delete=models.CASCADE)

    @property
    def status_percent_in_stock(self):
        p = int(self.in_stock / self.max_capacity * 100)
        if p < 20:
            return 100
        return p

    @property
    def status_color(self):
        p = int(self.in_stock / self.max_capacity * 100)
        if p < 20:
            return "rgba(100,0,0,20%)"
        elif p < 50:
            return "rgba(100,100,0,20%)"
        else:
            return "rgba(0,100,0,20%)"

class MachinePurchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

class RefillProcess(models.Model):
    datetime = models.DateTimeField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

class RefillItem(models.Model):
    field = models.ForeignKey(MachineField, on_delete=models.CASCADE)
    possible_to_refill = models.IntegerField()
    actual_refill = models.IntegerField()
