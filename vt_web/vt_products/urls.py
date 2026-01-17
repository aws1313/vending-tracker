from django.urls import path

from vt_products.views import MachineList, add_machine, MachineDetail, add_machine_row, add_machine_field, \
    ProductListView, ProductCreateView, ProductUpdateView, renew_api_key, MachineFieldUpdate, DashboardView

urlpatterns = [
    # DASHBOARD
    path("", DashboardView.as_view(), name="vt_products_dashboard"),
    # PRODUCTS
    path("products/", ProductListView.as_view(), name="vt_products_products"),
    path("products/add", ProductCreateView.as_view(), name="add_product"),
    path("products/update/<int:pk>", ProductUpdateView.as_view(), name="update_product"),


    # MACHINES
    path("machines/", MachineList.as_view(), name="vt_products_machines"),
    path("machines/add", add_machine),
    path("machines/<int:pk>", MachineDetail.as_view(), name="vt_machine_detail"),

    path("machines/<int:mid>/renew_api", renew_api_key),
    path("machines/<int:mid>/add_row", add_machine_row),
    path("machines/<int:mid>/<int:rid>/add_field", add_machine_field),
    path("machines/fields/update/<int:pk>", MachineFieldUpdate.as_view(), name="update_machine_field"),
]

