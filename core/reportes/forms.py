from django.forms import *
from core.erp.models import *
from django.contrib.auth.models import Group, ContentType, Permission

class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control input-flat',
        'autocomplete': 'off',
        'style': 'height: 35px;',
        'id': 'reservation'
    }))
    

class ReporUnidadForm(Form):
    # data = [{'id': '', 'text': ''}]
    # for i in Unidad.objects.filter(tipo_unidad='UAL'):
    #     data.append({'id': i.id, 'text': i.nombre})

   # data.append({'id': 100, 'text': 'TODAS'})

    unidad = ModelChoiceField(queryset=Unidad.objects.exclude(tipo_unidad='UADMC'), widget=Select(attrs={
         'class': 'form-control select2',
    }))

     
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'style': 'height: 32px;',
        'id': 'reservationUni'
    }))
    # unidad = CharField(widget=Select(attrs={
    #     'class': 'form-control float-right',
    #     'id': 'idunidad'    
    # }))

class ReporAlmacenForm(Form):
    almacen = ModelChoiceField(queryset=Almacen.objects.all(), widget=Select(attrs={
         'class': 'form-control input-flat',
         'style': 'height: 35px',
    }))

     
    categoria = ModelChoiceField(queryset=Categoria.objects.all(), widget=Select(attrs={
         'class': 'form-control input-flat',
         'style': 'height: 35px',
    }))

class FormAction(Form):
    CHOICES = [("NULL", "Seleccionar acción"), ("INACTIVE", "Inactivar"), ("ACTIVE", "Activar"), ("DELETE", "Eliminar")]
    action = ChoiceField(choices=CHOICES, widget=Select(attrs={
         'class': 'form-control input-flat',
         'style': 'height: 35px',
    }))


class FormModel(Form):
    content_type = ModelChoiceField(queryset=ContentType.objects.all(), widget=Select(attrs={
         'class': 'form-control input-flat',
         'style': 'height: 35px',
    }))
