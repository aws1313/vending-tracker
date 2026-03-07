import plotly.express as px
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from plotly.offline import plot

from vt_products.models import MachinePurchase


def wochen_umsatz_plot():
    data = (
        MachinePurchase.objects
        .filter(machine_id=1)
        .annotate(monat=TruncMonth("datetime"))
        .values("monat")
        .annotate(total_umsatz=Sum("price"))
        .order_by("monat")
    )
    fig = px.bar(
        data,
        x='monat',
        y='total_umsatz',
        labels={'monat': 'Zeitraum', 'total_umsatz': 'Umsatz (€)'},
        title="Monatliche Performance"
    )

    # 3. Layout-Feinschliff (optional)
    fig.update_layout(template="plotly_white")

    return plot(fig, output_type='div')
