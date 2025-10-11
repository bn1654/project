from django import forms
from .models import PolUser


# Форма для изменения данных пользователя
class ChangeUserInfo(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    
    
    class Meta:
        model = PolUser
        fields = ('username', 'email', 'first_name', 'last_name')


# Форма для изменения аватара пользователя
class AvatarChangeForm(forms.ModelForm):
    avatar = forms.ImageField(required=True, label='Аватар', allow_empty_file=False)
    
    class Meta:
        model = PolUser
        fields = ['avatar']