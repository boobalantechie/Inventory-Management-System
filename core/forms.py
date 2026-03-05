from django  import forms
from .models import Product,Category



class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        # fields=['category','name','price','quantity','image','status']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'enter name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder':'enter price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control','placeholder':'enter quantity'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['category'].empty_label = "Select Category"

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'enter category'})
        }
