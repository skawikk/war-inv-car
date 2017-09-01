from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.forms import IBANFormField
from localflavor.pl.forms import PLNIPField, PLPostalCodeField

from wesol.models import Invoices, Payments, ProductsInvoices, Products, Contractors


class PaymentsAddNewForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = "__all__"
        widgets = {
            'added_by': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["invoice"].queryset = Invoices.objects.filter(if_payment=False)


class ProductsInvoicesAddForm(forms.ModelForm):
    class Meta:
        model = ProductsInvoices
        fields = [
            "name",
            "quantity",
            "invoice",
            "date_expiration",
            "price_net",
        ]

        widgets = {
            'date_expiration': SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded = Invoices.objects.exclude(description__contains="Inwentaryzacja") & \
                   Invoices.objects.exclude(contractor__short_name__contains="Kas")
        self.fields["invoice"].queryset = excluded


class StocktakingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in Products.objects.filter(actual_quantity__gt=0):
            self.fields[i.name] = forms.IntegerField(widget=forms.TextInput)


class LoginForm(forms.Form):
    login = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data["login"]
        passwd = cleaned_data["password"]
        self.user = authenticate(username=login, password=passwd)
        if self.user is None:
            raise ValidationError("Błędne dane logowania!")
        return cleaned_data


class InvoicesAddNewForm(forms.ModelForm):
    class Meta:
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
        widgets = {
            'date_sale': SelectDateWidget(),
            'date_to_pay': SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        excluded = Contractors.objects.exclude(full_name__contains="Wewnętrzne:")
        self.fields["contractor"].queryset = excluded


class ContractorsNewAddForm(forms.ModelForm):
    nip = PLNIPField(label="NIP")
    postal_code = PLPostalCodeField(label="Kod pocztowy")
    bank_account = IBANFormField(include_countries=IBAN_SEPA_COUNTRIES, label="Nr konta bakowego")

    class Meta:
        model = Contractors
        exclude = ["added_by"]
