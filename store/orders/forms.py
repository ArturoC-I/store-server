from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите отчество'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': '685000, Магадан, Гаражный пер. 6А'}))

    class Meta:
        model = Order
        fields = ('first_name', 'surname', 'last_name', 'address')
