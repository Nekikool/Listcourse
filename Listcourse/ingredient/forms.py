from django import forms
from django.forms import ModelForm
from ingredient.models import List,ProductInList


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