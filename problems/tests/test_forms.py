from django.test import TestCase
from problems.forms import UserRegistrationForm, CodeSubmissionForm
from django.contrib.auth.models import User


class UserRegistrationFormTest(TestCase):
    """Testes para o formulário de registro"""
    
    def test_valid_registration_form(self):
        """Testa formulário válido"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_missing_username(self):
        """Testa formulário sem username"""
        form_data = {
            'email': 'test@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_registration_form_password_mismatch(self):
        """Testa senhas diferentes"""
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'complexpass123',
            'password2': 'differentpass'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_form_duplicate_username(self):
        """Testa username duplicado"""
        User.objects.create_user(username='existing', password='12345')
        form_data = {
            'username': 'existing',
            'email': 'new@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_form_invalid_email(self):
        """Testa email inválido"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_registration_form_email_required(self):
        """Testa se email é obrigatório"""
        form_data = {
            'username': 'testuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_registration_form_fields(self):
        """Testa campos do formulário"""
        form = UserRegistrationForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
    
    def test_registration_form_css_classes(self):
        """Testa se os campos têm a classe CSS correta"""
        form = UserRegistrationForm()
        for field_name, field in form.fields.items():
            self.assertEqual(field.widget.attrs.get('class'), 'form-control')


class CodeSubmissionFormTest(TestCase):
    """Testes para o formulário de submissão de código"""
    
    def test_valid_code_submission_form(self):
        """Testa formulário válido"""
        form_data = {
            'code': 'def solution():\n    return True'
        }
        form = CodeSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_code_submission_form_empty(self):
        """Testa formulário vazio"""
        form_data = {
            'code': ''
        }
        form = CodeSubmissionForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_code_submission_form_widget_attributes(self):
        """Testa atributos do widget"""
        form = CodeSubmissionForm()
        widget = form.fields['code'].widget
        self.assertEqual(widget.attrs.get('class'), 'form-control code-editor')
        self.assertEqual(widget.attrs.get('rows'), 20)
        self.assertIn('monospace', widget.attrs.get('style', ''))
    
    def test_code_submission_form_label(self):
        """Testa label do campo"""
        form = CodeSubmissionForm()
        self.assertEqual(form.fields['code'].label, 'Seu Código')
    
    def test_code_submission_form_accepts_multiline(self):
        """Testa se aceita código multilinha"""
        code = """def solution(a, b):
    result = a + b
    return result"""
        form_data = {'code': code}
        form = CodeSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertIn('def solution', form.cleaned_data['code'])
    
    def test_code_submission_form_with_special_characters(self):
        """Testa com caracteres especiais"""
        code = """
def solution(s):
    # Função com acentuação
    return s.replace('á', 'a')
"""
        form_data = {'code': code}
        form = CodeSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())

