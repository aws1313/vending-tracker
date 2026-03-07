from http import HTTPStatus

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, TemplateView, FormView
from django.views.generic.list import ListView
from django.shortcuts import render
from django import forms
from django.urls import reverse
from rest_framework_api_key.models import APIKey

from vt_products.models import Machine, MachineRow, MachineField, Product, ProductCategory, Purchase

from .plots import wochen_umsatz_plot


####
# DASHBOARD
####
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "vt_products/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context["purchases"] = Purchase.objects.filter(completed=False)

        #context["umsatz_plot"] = wochen_umsatz_plot()

        return context

####
# PRODUCTS
####
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    #def get_context_data(self, **kwargs):
    #    context = super(ProductListView, self).get_context_data(**kwargs)
    #    context["form"] = ProductForm()
    #    return context

#class ProductForm(LoginRequiredMixin, forms.Form):
#    name = forms.CharField(max_length=255)
#    price = forms.DecimalField(max_digits=10, decimal_places=2)
#    preview_image = forms.ImageField(required=False)
#    category = forms.ModelChoiceField(ProductCategory.objects.all())

class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = "__all__"
    success_url = "/dashboard/products"
    success_message = "Product successfully created"

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = "__all__"
    success_url = "/dashboard/products"
    success_message = "Product successfully updated"

class ProductCategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProductCategory
    fields = "__all__"
    success_url = "/dashboard/products"
    success_message = "Product category successfully created"

class ProductCategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ProductCategory
    fields = "__all__"
    success_url = "/dashboard/products"
    success_message = "Product category successfully updated"

@login_required()
def manage_categories(request):
    category_form_set = forms.modelformset_factory(ProductCategory, fields=["name"], can_delete=True, can_delete_extra=False, extra=5)
    if request.method == "POST":
        formset = category_form_set(request.POST, queryset=ProductCategory.objects.all())
        if formset.is_valid():
            formset.save()
        messages.success(request, f"Categories successfully updated")
        return HttpResponseRedirect("/dashboard/products")

    else:
        formset = category_form_set(queryset=ProductCategory.objects.all())

    return render(request, "vt_products/manage_product_categories.html", {"formset": formset})



# Purchase
class PurchaseView(LoginRequiredMixin, View):
    template_name = "vt_products/purchase.html"
    def get(self, request):
        context = {}



        return render(request, self.template_name, context=context)

    def post(self, request):
        context = {}
        return render(request, self.template_name, context=context)

####
# MACHINES
####
class MachineList(LoginRequiredMixin, ListView):
    model = Machine

class MachineDetail(LoginRequiredMixin, DetailView):
    model = Machine

class MachineAddForm(LoginRequiredMixin, forms.Form):
    friendly_name = forms.CharField(max_length=100)


class MachineFieldUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MachineField
    fields = ["product", "in_stock", "max_capacity"]
    success_message = "Field successfully updated"

    def get_success_url(self):
        return reverse("vt_machine_detail", kwargs={"pk": self.object.row.machine.id})


@login_required()
def add_machine(request):
    if request.method == "POST":
        form = MachineAddForm(request.POST)
        if form.is_valid():
            m = Machine.objects.create()
            m.friendly_name = form.cleaned_data["friendly_name"]
            m.save()

            return HttpResponseRedirect("/dashboard/machines")
    return HTTPStatus.BAD_REQUEST

@login_required()
def add_machine_row(request, mid):
    if request.method == "POST":
        MachineRow(machine_id=mid, chilled=False).save()
        return HttpResponseRedirect("/dashboard/machines/%s" % mid)

    return HTTPStatus.BAD_REQUEST

@login_required()
def add_machine_field(request, mid, rid):
    if request.method == "POST":
        MachineField(row_id=rid, max_capacity=10, in_stock=10).save()
        return HttpResponseRedirect("/dashboard/machines/%s" % mid)

    return HTTPStatus.BAD_REQUEST

@login_required()
def renew_api_key(request, mid):
    if request.method == "POST":
        m = Machine.objects.get(id=mid)
        if m.apikey:
            ap = m.apikey
            ap.revoked = True
            ap.save()
        api_key, key = APIKey.objects.create_key(name=f"Machine: {m.pk} - {m.friendly_name}")
        m.apikey = api_key
        m.save()
        messages.success(request, f"API-Key: {key}")
        return HttpResponseRedirect("/dashboard/machines/%s" % mid)


    return HTTPStatus.BAD_REQUEST