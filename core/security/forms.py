from django import forms
from core.security.models import *
from datetime import datetime

class BackupsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model=Backup
        fields = 'frequency', 'scheduled_date',
        widgets = {
            'frequency': forms.Select(
                attrs={
                    'class': 'form-control input-flat',                    
                    'id': 'idfrequen',
                    
                }
            ),
            'scheduled_date': forms.DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input input-flat',
                    'id': 'fecha_backup',
                    'data-target': '#fecha_backup',
                    'data-toggle': 'datetimepicker',
                    'style': 'height: 27px; font-size:11px;'
                }
            ),           
                                        
        }
        exclude = ['is_done']

class BackupForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))