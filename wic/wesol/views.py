from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView

from wesol.forms import PaymentsAddNewForm
from wesol.mixins import GetInitialAuthorMixin
from wesol.models import Invoices


class InvoicesAddNewView(CreateView):
    model = Invoices
    fields = [
        "number",
        "contractor",
        "gross",
        "date_sale",
        "date_to_pay",
        "if_payment",
        "description",
    ]
    template_name = "wesol/generic_form.html"

    def form_valid(self, form):
        # redirect to specyfic URL if checkbox _if_payment is selected:
        if form.cleaned_data["if_payment"]:
            self.success_url = "/payment-add"
        else:
            self.success_url = "/"
        # set added_by to current logged user:
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class PaymentAddNewView(GetInitialAuthorMixin, CreateView):
    form_class = PaymentsAddNewForm
    template_name = "wesol/generic_form.html"
    success_url = "/"
