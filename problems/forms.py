from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    """Formulário de registro de usuário"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, required=False, label='Nome')
    last_name = forms.CharField(max_length=100, required=False, label='Sobrenome')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes CSS aos campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CodeSubmissionForm(forms.Form):
    """Formulário para submissão de código"""
    code = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control code-editor',
            'rows': 20,
            'style': 'font-family: monospace;'
        }),
        label='Seu Código'
    )

