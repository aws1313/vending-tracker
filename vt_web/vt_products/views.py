from http import HTTPStatus

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django import forms
from vt_products.models import Machine, MachineRow, MachineField, Product, ProductCategory


####
# PRODUCTS
####
class ProductListView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context["form"] = ProductForm()
        return context

class ProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    preview_image = forms.ImageField(required=False)
    category = forms.ModelChoiceField(ProductCategory.objects.all())

class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    fields = "__all__"
    success_url = "/dashboard/products"
    success_message = "Product successfully created"

class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    fields = "__all__"
    success_url = "/dashboard/products"
    success_message = "Product successfully updated"


####
# MACHINES
####
class MachineList(ListView):
    model = Machine

class MachineDetail(DetailView):
    model = Machine

class MachineAddForm(forms.Form):
    friendly_name = forms.CharField(max_length=100)

def add_machine(request):
    if request.method == "POST":
        form = MachineAddForm(request.POST)
        if form.is_valid():
            m = Machine.objects.create()
            m.friendly_name = form.cleaned_data["friendly_name"]
            m.save()

            return HttpResponseRedirect("/dashboard/machines")
    return HTTPStatus.BAD_REQUEST

def add_machine_row(request, mid):
    if request.method == "POST":
        MachineRow(machine_id=mid, chilled=False).save()
        return HttpResponseRedirect("/dashboard/machines/%s" % mid)

    return HTTPStatus.BAD_REQUEST

def add_machine_field(request, mid, rid):
    if request.method == "POST":
        MachineField(row_id=rid, max_capacity=10, in_stock=10).save()
        return HttpResponseRedirect("/dashboard/machines/%s" % mid)

    return HTTPStatus.BAD_REQUEST