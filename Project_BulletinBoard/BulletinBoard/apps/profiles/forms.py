from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from allauth.account.forms import LoginForm, PasswordField, SignupForm
from allauth.utils import set_form_field_order


class CustomLoginForm(LoginForm):
    password = PasswordField(label='Пароль', autocomplete='current-password')
    password_widget = forms.PasswordInput(
            attrs={'placeholder': 'Пароль',
                   'class': 'form-control'},
        )
    password.widget = password_widget
    error_messages = {
        'account_inactive': 'Этот аккаунт в настоящее время неактивен.',
        'email_password_mismatch': 
            'Некорректный адрес электронной почты или пароль.'
        ,
        'username_password_mismatch': 
            'Некорректное имя пользователя или пароль.'
        ,
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        login_widget = forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder': 'Электронная почта',
                'autocomplete': 'email',
            }
        )
        login_field = forms.EmailField(label='Электронная почта', widget=login_widget)
        self.fields['login'] = login_field
        set_form_field_order(self, ['login', 'password'])
        self.fields['password'].help_text = mark_safe(
            '<a href="{}">Забыли пароль?</a>').format(
                reverse('account_reset_password')
        )


class CustomSignupForm(SignupForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        password1 = PasswordField(
            label='Пароль',
            autocomplete='new-password',
        )
        password1_widget = forms.PasswordInput(
            attrs={'placeholder': 'Пароль',
                   'class': 'form-control'},
        )
        password1.widget = password1_widget
        password2 = PasswordField(
                label='Пароль (повтор)', autocomplete='new-password'
            )
        password2_widget = forms.PasswordInput(
            attrs={'placeholder': 'Повторите пароль',
                   'class': 'form-control'},
        )
        password2.widget = password2_widget
        email = forms.EmailField(
            widget=forms.TextInput(
                attrs={
                    'type': 'email',
                    'class': 'form-control',
                    'placeholder': 'Электронная почта',
                    'autocomplete': 'email',
                }
            )
        )
        self.fields['email'] = email
        self.fields['email'].label = 'Электронная почта'
        self.fields['password1'] = password1
        self.fields['password2'] = password2
        set_form_field_order(self, ['email', 'password1', 'password2'])

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        common_group = Group.objects.get_or_create(name='common')[0]
        common_group.user_set.add(user)
        username = User.objects.get(username=user)
        User.objects.filter(username=user).update(first_name=str(username))
        return user
