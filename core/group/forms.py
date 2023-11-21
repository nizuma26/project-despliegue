from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group, ContentType, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple


class FormGroup(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ids_exclude = ['logentry', 'contenttype', 'session', 'dettrasladoprod', 'detsalidainsumos', 'detingresoproduc', 'detdesincprod', 'detdesincalmacen', 'permission', 'detsalidaprod', 'detsolicsoporte', 'inventariobienes', 'seriales', 'lotes']
        self.fields['permissions'].queryset = Permission.objects.exclude(content_type__model__in=ids_exclude)

    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese un nombre',
                    'id': 'name',
                }
            ),
            'permissions': forms.SelectMultiple(
                attrs={
                    'class': 'form-control duallistbox',
                    'style': 'height: 250px;',
                    'multiple': 'multiple',
                    'id': 'idperm',
                }
            ),                       
        }
       
    def save(self, commit=True):
        data = {}
        form = super()
      #  __AUTOCODE__="COM"
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    
       
   
