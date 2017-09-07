from django.contrib.auth.models import User
from django.db import models
from localflavor.pl.forms import PLNIPField

from .choices import (
    ACCOUNT_TYPE_CHOICES,
    PAYMENTS_TYPE_CHOICES,
    PRODUCTS_TAX_CHOICES,
    PRODUCTS_USED_IN_CHOICES
)


class Accounts(models.Model):
    name = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES, verbose_name="Nazwa")
    number = models.CharField(max_length=28, verbose_name="Numer konta")

    def __str__(self):
        return str(self.get_name_display())


class Contractors(models.Model):
    short_name = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Skrót nazwy"
    )
    full_name = models.CharField(max_length=128, verbose_name="Pełna nazwa")
    nip = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[]
    )

    street = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="Ulica"
    )
    city = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="Miasto"
    )
    postal_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name="Kod pocztowy"
    )
    bank_account = models.CharField(
        max_length=28,
        null=True,
        blank=True,
        verbose_name="Nr konta"
    )
    added_by = models.ForeignKey(User)

    def __str__(self):
        return self.short_name


class Invoices(models.Model):
    number = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Numer faktury"
    )
    contractor = models.ForeignKey(Contractors, verbose_name="Kontrahent")
    gross = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Wartość faktury"
    )
    date_sale = models.DateField(verbose_name="Terin wystawienia")
    date_to_pay = models.DateField(verbose_name="Termin płatności")
    if_payment = models.BooleanField(default=False, verbose_name="Czy opłacona")
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Opis"
    )
    date_added = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    if contractor:
        contractor = contractor
    else:
        contractor = "brak"

    def __str__(self):
        return "{} nr: {}".format(
            self.contractor,
            self.number,
        )


class Payments(models.Model):
    type = models.IntegerField(choices=PAYMENTS_TYPE_CHOICES, verbose_name="Rodzaj płatności")
    invoice = models.ForeignKey(
        Invoices,
        null=True,
        blank=True,
        verbose_name="Faktura"
    )
    contractor = models.ForeignKey(
        Contractors,
        null=True,
        blank=True,
        verbose_name="Kontrahent"
    )
    account = models.ForeignKey(Accounts, verbose_name="Konto")
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Opis"
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Wartość"
    )
    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return "{} {} {}".format(self.get_type_display(), self.date, self.value)


class Products(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Nazwa"
    )
    tax = models.IntegerField(choices=PRODUCTS_TAX_CHOICES, verbose_name="Stawka VAT")
    used_in = models.IntegerField(
        choices=PRODUCTS_USED_IN_CHOICES,
        null=True,
        blank=True,
        verbose_name="Przeznaczenie"
    )
    actual_quantity = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class ProductsInvoices(models.Model):
    name = models.ForeignKey(Products, verbose_name="Produkt")
    quantity = models.IntegerField(verbose_name="Ilość")
    invoice = models.ForeignKey(Invoices, verbose_name="Faktura")
    date_added = models.DateField(auto_now_add=True)
    date_expiration = models.DateField(
        null=True,
        blank=True,
        verbose_name="Termin ważności"
    )
    price_net = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Cena netto"
    )
    quantity_remaining = models.IntegerField()
    added_by = models.ForeignKey(User)

    def __str__(self):
        return "{}".format(self.name)


class DailyReport(models.Model):
    number = models.CharField(max_length=10, verbose_name="Numer raportu")
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Kwota"
    )
    cash = models.ForeignKey(Payments)
    credit_card_take = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Karty płatnicze"
    )
    counted_money_in_drawer = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Kwota w szufladzie"
    )
    added_by = models.ForeignKey(User)

    def __str__(self):
        return "Rap. nr: {}, {}zł".format(self.number, self.value)
