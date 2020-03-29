from django import forms

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class AddProductForm(forms.Form):

    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.TypedChoiceField(coerce=int, choices=QUANTITY_CHOICES)

    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)