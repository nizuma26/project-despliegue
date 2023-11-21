from django import forms
from core.aprobaciones.models import *
from datetime import datetime

class ManageRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Aprobaciones
        fields = '__all__'
        widgets = {
            'accion': forms.Select(
                attrs={                   
                    'autofocus': True,
                    'id': 'action_request'
                }
            ),            
            'motivo': forms.Textarea(
                attrs={                    
                    'rows': '6',                    
                    'autocomplete': 'off',
                    'id': 'motive'
                }
            ),           
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                 form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
