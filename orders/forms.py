from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'checkout-input',
                'placeholder': 'Adınız',
                'autocomplete': 'given-name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'checkout-input',
                'placeholder': 'Soyadınız',
                'autocomplete': 'family-name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'checkout-input',
                'placeholder': 'ornek@email.com',
                'autocomplete': 'email',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'checkout-input checkout-textarea',
                'placeholder': 'Mahalle, Cadde, Sokak, Bina No, Daire...',
                'rows': 3,
                'autocomplete': 'street-address',
                'required': True
            }),
            'city': forms.TextInput(attrs={
                'class': 'checkout-input',
                'placeholder': 'Örn: İstanbul',
                'autocomplete': 'address-level2',
                'required': True
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'checkout-input',
                'placeholder': '34000',
                'autocomplete': 'postal-code',
                'required': True
            }),
        }