# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelForm,Textarea
from ingredient.models import List,ProductInList, Product


class AddProductToListForm(ModelForm):
    class Meta:
        model = ProductInList
        fields = ['quantity']

    # def __init__(self, *args, **kwargs):
    #     super(AddProductToListForm, self).__init__(*args, **kwargs)
    #     self.fields['product'].label_from_instance = lambda obj: "%s" % (obj.name)

class CreateListForm(ModelForm):
    class Meta:
        model = List
        fields = ['name']


class AddCustomProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['user','perso']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5}),
        }
        labels = {
            'name': ('Nom du produit'),
            'subCategory': ('Sous-catégorie'),
        }

    def __init__(self, *args, **kwargs):
        super(AddCustomProductForm, self).__init__(*args, **kwargs)
        self.fields['subCategory'].label_from_instance = lambda obj: "%s" % (obj.name)


# class AddProductToListForm(forms.Form):
#     productId = forms.CharField(required=True)
#     quantite = forms.IntegerField(required=True, default=0)
  
    # def __init__(self, *args, **kwargs):
    #     self.request  = kwargs.pop('request', None)
    #     super(CreateListForm, self).__init__(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     kwargs['commit']=False
    #     obj = super(CreateListForm, self).save(*args, **kwargs)
    #     if self.request:
    #         obj.user = self.request.user
    #     obj.save()
    #     return obj