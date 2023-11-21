from django import forms
from django.forms import ModelForm
from core.user.models import User
from django.contrib.auth.models import Permission


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        #self.fields['user_permissions'].queryset = Permission.objects.all().values_list('name', flat=True)
        # Aquí puedes modificar el widget del campo de imagen
        self.fields['image'].widget = forms.ClearableFileInput(attrs={'accept': 'image/*'})

    class Meta:
        model = User
        fields = 'first_name', 'last_name','dni', 'email', 'username', 'password', 'image', 'groups', 'is_active' 
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'id': 'idnombre',  
                    'class': 'input-style form-control',
                    'autofocus': True
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',                    
                    'class': 'input-style form-control',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su cédula',                    
                    'class': 'input-style form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',                    
                    'class': 'input-style form-control',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                    'autocomplete': 'off',
                    'id': 'iduser',
                    'class': 'input-style form-control'
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese su password',
                    'class': 'input-style form-control',
                }
            ),            
            'image': forms.FileInput(
                attrs = {
                    'placeholder': 'Seleccione Imagen ...',
                    'class': 'form-control',
                    'id': 'seleccionArchivos',
                    'style': 'font-size: 12px'
                }
            ), 
            'groups': forms.SelectMultiple(attrs={
                'class': 'select2',
                'style': 'width: 100%;',
                'multiple': 'multiple',
                'id': 'idgroups',
                # 'data-dropdown-css-class': 'select2-gray',
                'data-placeholder': 'Buscar..'
                
                }
            ),            
            'is_active': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',                
                'id': 'idactive',               
                }
            ),                 
                       
        }
        exclude = ['last_login', 'date_joined', 'is_superuser', 'is_staff', 'user_permissions']
        #CheckboxSelectMultiple
    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             print(self.cleaned_data['user_permissions'])
    #             pwd = self.cleaned_data['password']
    #             u = form.save(commit=False)
    #             if u.pk is None:
    #                 u.set_password(pwd)
    #             else:
    #                 user = User.objects.get(pk=u.pk)
    #                 if user.password != pwd:
    #                     u.set_password(pwd)
    #             u.save()
    #             u.groups.clear()
    #             for g in self.cleaned_data['groups']:
    #                 u.groups.add(g)
                    
    #             u.user_permissions.clear()                
    #             for p in self.cleaned_data['user_permissions']:
    #                 u.user_permissions.add(p)
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'image', 'password', 'dni'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'autocomplete': 'off',
                    'required': True
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'autocomplete': 'off',
                    'required': True
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'autocomplete': 'off',
                    'required': True
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'autocomplete': 'off',
                    'required': True
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'placeholder': 'Seleccione Imagen ...',
                    'class': 'form-control',
                    'id': 'seleccionArchivos',
                    'style': 'font-size: 12px',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                attrs={
                    'required': True
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'required': True
                }
            ),            
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

