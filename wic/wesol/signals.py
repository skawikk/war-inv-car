from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from wesol.models import Payments, Invoices

# receviers to check gross of invoices, and if payment covers the amount of invoice
# set if_payment field to True (it will hope to create payments and list for invoices without a payment

@receiver(post_save, sender=Payments)
def check_ivoice_payments(sender, **kwargs):
    if kwargs.get('created', True):
        id_inv = kwargs['instance'].invoice.id
        payments_list_by_invoice = Payments.objects.all().filter(invoice__id=id_inv)
        sum_payments = payments_list_by_invoice.aggregate(t=Sum("value"))["t"]
        invoice_gross = Invoices.objects.get(id=id_inv).gross
        if sum_payments == invoice_gross:
            invoice = Invoices.objects.get(id=id_inv)
            invoice.if_payment = True
            invoice.save()