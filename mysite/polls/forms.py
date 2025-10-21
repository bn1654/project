from django import forms
from django.forms import inlineformset_factory
from .models import PolUser, Question, Choice
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class CreatePoll(forms.ModelForm):
    question_text = forms.CharField(label='Вопрос', required=True)
    
    def save(self, commit = True):
            question = super().save(commit=False)
            question.short_description_former()
            if commit:
                question.save()
            return question
    
    class Meta:
            model = Question
            fields = ['question_text', 'description', 'image',]

ChoiceFormSet = inlineformset_factory(Question, Choice, fields=['choice_text'])

class RegisterUserForm(forms.ModelForm):
        email = forms.EmailField(required=True, label='Адрес электронной почты')
        avatar = forms.ImageField(required=True, label='Аватар', allow_empty_file=False)
        password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
        password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Повторите пароль')
        
        def clean_password(self):
            password1 = self.cleaned_data['password1']
            if password1:
                password_validation.validate_password(password1)
            return password1
        
        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data['password1']
            password2 = cleaned_data['password2']  
            if password1 and password2 and password1 != password2:
                errors = {'password2': ValidationError('Введнные данные пользователем не совпадают', code='password_mismatch')}
                raise ValidationError

            return cleaned_data
        
        
        def save(self, commit = True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.is_active = True
            
            if commit:
                user.save()
            return user
        
        class Meta:
            model = PolUser
            fields = ['username', 'email', 'avatar', 'password1', 'password2', 'first_name', 'last_name']
            
    
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