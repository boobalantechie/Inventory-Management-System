from django  import forms
from .models import Product,Category



class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        # fields=['category','name','price','quantity','image','status']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }