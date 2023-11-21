from datetime import datetime
from django import forms
from django.contrib.auth import authenticate
from core.security.choices import LOGIN_TYPE
from core.security.models import AccessUsers
from core.user.models import User


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        # 'placeholder': 'Ingrese su nombre de usuario',
        'style': 'font-size: 13px;',        
        'autocomplete': 'off',
        'required': True,
        'id': 'user'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # 'placeholder': 'Ingrese su contraseña',        
        'style': 'font-size: 13px;',        
        'autocomplete': 'off',
        'name': 'password',
        'required': True,
        'id': 'password'
    }))

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '')
        password = cleaned.get('password', '')
        if len(username) == 0:
            raise forms.ValidationError('Ingrese su username')
        elif len(password) == 0:
            raise forms.ValidationError('Ingrese su password')

        queryset = User.objects.filter(username=username).prefetch_related('user_permissions').prefetch_related('groups')
        if queryset.exists():
            user = queryset[0]
            if not user.is_active:
                raise forms.ValidationError('El usuario ha sido bloqueado. Comuníquese con su administrador.')
            if authenticate(username=username, password=password) is None:
                AccessUsers(user=user, type=LOGIN_TYPE[1][0]).save()
                intent = user.accessusers_set.filter(type=LOGIN_TYPE[1][0], date_joined=datetime.now().date()).count()
                if intent > 2:
                    user.is_active = False
                    user.save()
                    raise forms.ValidationError('El usuario ha sido bloqueado por superar el límite de intentos fallidos en un día.')
                count = 3 - intent
                raise forms.ValidationError(f"La contraseña ingresada es incorrecta, por favor intentelo de nuevo. Le quedan {count} {'intento' if count == 1 else 'intentos'}. Si supera los 3 intentos fallidos su cuenta sera bloqueada.")
            AccessUsers(user=user).save()
            return cleaned
        raise forms.ValidationError('Por favor introduzca el nombre de usuario y la clave correctos para una cuenta de personal. Observe que ambos campos pueden ser sensibles a mayúsculas.')

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'font-size: 13px; font-weight: 530',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            self._errors['error'] = self._errors.get('error', self.error_class())
            self._errors['error'].append('El usuario no existe')
            # raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese su contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita la contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned
