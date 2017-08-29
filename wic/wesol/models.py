from django.contrib.auth.models import User
from django.db import models
from .choices import (
    ACCOUNT_TYPE_CHOICES,
    PAYMENTS_TYPE_CHOICES,
    PRODUCTS_TAX_CHOICES,
    PRODUCTS_USED_IN_CHOICES
)


class Accounts(models.Model):
    name = models.IntegerField(choices=ACCOUNT_TYPE_CHOICES)
    number = models.CharField(max_length=28)

    def __str__(self):
        return str(self.get_name_display())


class Contractors(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=128)
    nip = models.IntegerField(null=True, blank=True)
    street = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    bank_account = models.CharField(max_length=28, null=True, blank=True)

    def __str__(self):
        return self.short_name


class Invoices(models.Model):
    number = models.CharField(max_length=128, unique=True)
    contractor = models.ForeignKey(Contractors)
    gross = models.DecimalField(max_digits=10, decimal_places=2)
    date_sale = models.DateField()
    date_to_pay = models.DateField()
    if_payment = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return "{}:{}:{}".format(self.contractor, self.number, self.if_payment)


class Payments(models.Model):
    type = models.IntegerField(choices=PAYMENTS_TYPE_CHOICES)
    invoice = models.ForeignKey(Invoices, null=True, blank=True)
    contractor = models.ForeignKey(Contractors, null=True, blank=True)
    account = models.ForeignKey(Accounts)
    description = models.TextField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return "{} {} {}".format(self.get_type_display(), self.date, self.value)


class Products(models.Model):
    name = models.CharField(max_length=64, unique=True)
    tax = models.IntegerField(choices=PRODUCTS_TAX_CHOICES)
    used_in = models.IntegerField(choices=PRODUCTS_USED_IN_CHOICES, null=True, blank=True)
    invoice = models.ManyToManyField(
        Invoices,
        through="ProductsInvoices",
        related_name="products"
    )

    def __str__(self):
        return self.name


class ProductsInvoices(models.Model):
    name = models.ForeignKey(Products)
    quantity = models.IntegerField()
    invoice = models.ForeignKey(Invoices)
    date_added = models.DateField(auto_now_add=True)
    date_expiration = models.DateField()
    price_net = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "{}".format(self.name)
