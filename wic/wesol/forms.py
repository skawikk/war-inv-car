from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from wesol.models import Invoices, Payments, ProductsInvoices, Products


class PaymentsAddNewForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = "__all__"
        widgets = {'added_by': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        # TODO: add exlude field from form if user has no perm!!
        # user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields["invoice"].queryset = Invoices.objects.filter(if_payment=False)
        # if not user.is_staff:
        #     del self.fields['contractor']


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["invoice"].queryset = Invoices.objects.exclude(description__contains="Inwentaryzacja")


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
