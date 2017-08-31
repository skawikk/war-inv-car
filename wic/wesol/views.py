from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, FormView

from wesol.forms import PaymentsAddNewForm, StocktakingForm, ProductsInvoicesAddForm, LoginForm
from wesol.mixins import GetInitialAuthorMixin
from wesol.models import Invoices, DailyReport, Payments, Products, ProductsInvoices


class InvoicesAddNewView(LoginRequiredMixin, CreateView):
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
        invoice = form.save(commit=False)
        invoice.added_by = self.request.user
        invoice.save()
        return redirect(self.success_url)


class PaymentAddNewView(LoginRequiredMixin, GetInitialAuthorMixin, CreateView):
    form_class = PaymentsAddNewForm
    template_name = "wesol/generic_form.html"
    success_url = "/"


class DailyReportAddNewView(LoginRequiredMixin, CreateView):
    model = DailyReport
    fields = [
        "number",
        "value",
        "credit_card_take",
        "counted_money_in_drawer",
    ]
    template_name = "wesol/generic_form.html"
    success_url = "/"

    def form_valid(self, form):
        date = datetime.today().strftime("%d-%m-%Y")
        desc = "Utarg z dnia {}, raport dobowy fiskalny nr {}"
        cash = form.cleaned_data["value"] - form.cleaned_data["credit_card_take"]
        # set added_by to current logged user:
        report = form.save(commit=False)
        report.added_by = self.request.user
        # add payment to Payments:
        payment = Payments(
            type=1,
            contractor_id=2,
            account_id=5,
            description=desc.format(date, form.cleaned_data["number"]),
            value=cash,
            added_by=self.request.user,
        )
        # save daily report and payment:
        payment.save()
        report.cash = payment
        report.save()
        return redirect(self.success_url)


class ProductNewAddView(LoginRequiredMixin, CreateView):
    model = Products
    fields = [
        "name",
        "tax",
        "used_in",
    ]
    template_name = "wesol/generic_form.html"
    success_url = "#"


class ProductsInvoiceAddView(LoginRequiredMixin, CreateView):
    form_class = ProductsInvoicesAddForm
    template_name = "wesol/generic_form.html"
    success_url = "/"

    def get_initial(self):
        initial = super().get_initial()
        initial.copy()
        initial["invoice"] = Invoices.objects.exclude(description__contains="Inwentaryzacja").order_by("id").last()
        return initial

    def form_valid(self, form):
        product_invoice = form.save(commit=False)
        product_invoice.quantity_remaining = form.cleaned_data["quantity"]
        product_invoice.added_by = self.request.user
        product_invoice.save()
        product_quantity = Products.objects.get(name=form.cleaned_data["name"])
        product_quantity.actual_quantity += form.cleaned_data["quantity"]
        product_quantity.save()
        return redirect(self.success_url)


class StocktakingView(LoginRequiredMixin, View):
    form_class = StocktakingForm
    template_name = "wesol/generic_form.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {
            "form": form,
        })

    def post(self, request):
        form = StocktakingForm(data=request.POST)
        if form.is_valid():
            stocktake_gross = 0
            # change left quantity of product in specific register
            for key, value in form.cleaned_data.items():
                product_id = Products.objects.get(name=key).id
                product_all_in_warehouse = ProductsInvoices.objects. \
                    filter(name_id=product_id). \
                    filter(quantity_remaining__gt=0). \
                    order_by("date_added")
                product_quantity_all_in_warehouse = product_all_in_warehouse.aggregate(
                    Sum("quantity_remaining")
                )["quantity_remaining__sum"]
                product_quantity_stocktake_left = value
                product_diff = product_quantity_all_in_warehouse - product_quantity_stocktake_left
                while product_diff > 0:
                    product_to_change = product_all_in_warehouse.first()
                    print(product_to_change, product_to_change.pk)
                    if product_diff > product_to_change.quantity_remaining:
                        product_diff -= product_to_change.quantity_remaining
                        stocktake_gross += product_to_change.price_net * product_to_change.quantity_remaining
                        product_to_change.quantity_remaining = 0
                        product_to_change.save()
                    else:
                        stocktake_gross += product_to_change.price_net * product_diff
                        product_to_change.quantity_remaining -= product_diff
                        product_to_change.save()
                        product_diff = 0

            stocktake_invoice = Invoices(
                number="{}".format(datetime.today().strftime("%m/%Y")),
                contractor_id=6,
                gross=stocktake_gross,
                date_sale=datetime.now().strftime("%Y-%m-%d"),
                date_to_pay=datetime.now().strftime("%Y-%m-%d"),
                if_payment=True,
                description="Inwentaryzacja z dnia {}".format(datetime.today().strftime("%d-%m-%Y")),
                added_by=self.request.user,
            )
            stocktake_invoice.save()
            for key, value in form.cleaned_data.items():
                inv_id = Products.objects.get(name=key).id
                price_net = ProductsInvoices.objects.filter(name_id=inv_id). \
                    filter(quantity_remaining__gt=0). \
                    order_by("date_added"). \
                    aggregate(Avg("price_net"))["price_net__avg"]
                print(price_net)
                product_stocktake = Products.objects.get(name=key)
                # Add ProductsInvoice record for each product:
                product_invoice = ProductsInvoices(
                    name_id=Products.objects.get(name=key).id,
                    quantity=product_stocktake.actual_quantity - value,
                    invoice=stocktake_invoice,
                    price_net=price_net,
                    quantity_remaining=0,
                    added_by=self.request.user,
                )
                # Update quantity in Products:
                product_stocktake.actual_quantity = value
                product_stocktake.save()
                product_invoice.save()
        return redirect("/")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "wesol/generic_form.html"

    def form_valid(self, form):
        login(self.request, form.user)
        return redirect(self.request.GET.get("next", "/"))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class HomeSiteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "base.html")
