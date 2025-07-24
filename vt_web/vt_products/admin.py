from django.contrib import admin
from vt_products.models import ProductCategory, Product, Machine, Batch, MachineRow, MachineField, Purchase

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Batch)
admin.site.register(Purchase)

admin.site.register(Machine)
admin.site.register(MachineRow)
admin.site.register(MachineField)
