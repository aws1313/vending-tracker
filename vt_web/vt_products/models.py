from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    preview_image = models.ImageField()
    vend_price = models.DecimalField(max_digits=10, decimal_places=2)

class Purchase(models.Model):
    datetime = models.DateTimeField()

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    pieces = models.IntegerField()
    expiration_date = models.DateField()
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)


class Machine(models.Model):
    friendly_name = models.CharField(max_length=255)


class MachineRow(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    chilled = models.ForeignKey(Product, on_delete=models.CASCADE)

class MachineField(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    max_capacity = models.IntegerField()
    in_stock = models.IntegerField()
    row = models.ForeignKey(MachineRow, on_delete=models.CASCADE)

class MachinePurchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    datetime = models.DateTimeField()