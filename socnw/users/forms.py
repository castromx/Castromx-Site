from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

# Форма для реєстрації
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор паролю', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Форма для авторизації
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

# Форма для новин
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        if self.instance.pk:  # Якщо новина вже існує (редагування), заборонити зміну фотографії
            self.fields['image'].widget.attrs['disabled'] = 'disabled'

    title = forms.CharField(max_length=255, label='Заголовок', required=True)
    content = forms.CharField(widget=forms.Textarea, label='Зміст', required=True)
    image = forms.ImageField(label='Зображення', required=False)  # Поле зображення не обов'язкове

# Форма для коментарів
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

# Форма для опису профілю
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['status', 'birth_date', 'workplace', 'wishes']

    status = forms.CharField(label='Статус')
    birth_date = forms.DateField(label='Дата народження')
    workplace = forms.CharField(label='Місце роботи/навчання')
    wishes = forms.CharField(label='Бажання')