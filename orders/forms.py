from django import forms

class OrderForm(forms.Form):
    shipping_address = forms.CharField(
        label="Dirección de envío",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu dirección completa'})
    )
    
    PAY_METHODS = (
        ('CREDIT', 'Tarjeta de Crédito'),
        ('DEBIT', 'Tarjeta de Débito'),
        ('PAYPAL', 'PayPal'),
        ('CASH', 'Efectivo'),
        ('TRANSFER', 'Transferencia Bancaria'),
    )

    pay_method = forms.ChoiceField(
        label="Método de pago",
        choices=PAY_METHODS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )