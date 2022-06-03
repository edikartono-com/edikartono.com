from django import forms
from django.forms import ModelForm

from corecode.validation import only_latters
from products import models as pmd

class FormCreateProducts(ModelForm):
    class Meta:
        model = pmd.Product
        exclude = ['slug']
    
    def __init__(self, *args, **kwargs):
        super(FormCreateProducts, self).__init__(*args, **kwargs)
        self.fields['name'].validators = [only_latters]