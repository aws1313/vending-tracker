import django_filters
from .models import Product, ProductCategory
from django.db.models import Q

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="search_name_or_ean",
        label="Search",

    )

    category = django_filters.ModelChoiceFilter(
        queryset=ProductCategory.objects.all(),
        empty_label="Select Category",
    )

    class Meta:
        model = Product
        fields = ["search", "category",]

    def search_name_or_ean(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(ean__icontains=value)
        )