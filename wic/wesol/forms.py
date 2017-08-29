from django import forms

from wesol.models import Invoices, Payments

# class InvoicesAddNewForm(forms.ModelForm)
#     class Meta:
#         model = Invoices
#         fields =


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
