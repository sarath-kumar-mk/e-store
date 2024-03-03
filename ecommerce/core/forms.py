from django import forms
from core.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'desc':forms.Textarea(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'product_available_count':forms.NumberInput(attrs={'class':'form-control'}),
            'img':forms.FileInput(attrs={'class':'form-control'}),
            
        }

class CheckoutForm(forms.Form):
    street_address=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'1234 Main St'
    }))
    
    apartment_address=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Apartment or sits'
    }))
    
    # country = CountryField(
    #     blank_label="(select country)"
    # ).formfield(
    #     widget=forms.Select(attrs={'class': 'custom-select d-block w-100'})
    country=forms.CharField(required=False,widget=forms.TextInput(attrs={
    'class':'form-control',
    'placeholder':'Apartment or sits'
}))

    zip_code=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    
    # country=CountryField(blank_label="(select country)").formfield(widget=CountrySelectwidget.forms.ChoiceField(attrs{class:'custom-select d-block w-100'}))
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =["category_name"]
        # widgets = {
        #     'category_name':forms.Select(attrs={'class':'form-control'}),
            
            
        # }
