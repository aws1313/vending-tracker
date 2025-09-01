from django.urls import path

from vt_products.views import MachineList, add_machine, MachineDetail, add_machine_row, add_machine_field, \
    ProductListView, ProductCreateView, ProductUpdateView

urlpatterns = [
    # PRODUCTS
    path("products/", ProductListView.as_view(),),
    path("products/add", ProductCreateView.as_view(), name="add_product"),
    path("products/update/<int:pk>", ProductUpdateView.as_view(), name="update_product"),


    # MACHINES
    path("machines/", MachineList.as_view()),
    path("machines/add", add_machine),
    path("machines/<int:pk>", MachineDetail.as_view()),
    path("machines/<int:mid>/add_row", add_machine_row),
    path("machines/<int:mid>/<int:rid>/add_field", add_machine_field)
]

