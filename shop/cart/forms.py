from django import forms
from django.core.exceptions import ValidationError

from main.models import Order, VirtualOrder


class CartAddProductForm(forms.Form):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class ComparisonAddProductForm(forms.Form):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class FavoritesAddProductForm(forms.Form):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class RecentlyViewedProductForm(forms.Form):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class VirtualOrderForm(forms.ModelForm):
    class Meta:
        model = VirtualOrder
        fields = ('phone',)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone)) != 12 or str(phone)[:3] != '375':
            raise ValidationError('Номер должен быть равен 12 символов и в формате 375**')
        return phone


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products', 'price', 'user', 'state']
