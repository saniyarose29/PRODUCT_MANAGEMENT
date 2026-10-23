from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'sku',
            'category',
            'price',
            'stock',
            'image',
            'description',
            'status',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter product name'
                }
            ),

            'sku': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter SKU'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter price',
                    'step': '0.01'
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter stock quantity'
                }
            ),

            'image': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Paste image URL'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter product description'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price <= 0:
            raise forms.ValidationError(
                'Price must be greater than 0.'
            )

        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if stock is not None and stock < 0:
            raise forms.ValidationError(
                'Stock cannot be negative.'
            )

        return stock