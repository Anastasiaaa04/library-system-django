from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book, Author, Genre, Reader, BookReview


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите email'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })


class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))


class BookSearchForm(forms.Form):
    """Форма поиска книг (реализована через Django Forms)"""
    title = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию...'
        })
    )
    author = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по автору...'
        })
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label="Все жанры",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_year = forms.IntegerField(
        required=False,
        min_value=1000,
        max_value=2100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От года'
        })
    )
    max_year = forms.IntegerField(
        required=False,
        min_value=1000,
        max_value=2100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До года'
        })
    )
    min_rating = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Мин. рейтинг',
            'step': '0.1'
        })
    )


class BookReviewForm(forms.ModelForm):
    """Форма отзыва о книге (реализована через Django Forms)"""
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'range',
            'min': '1',
            'max': '5',
            'step': '1',
            'oninput': "this.nextElementSibling.value = this.value"
        })
    )
    rating_display = forms.CharField(
        label='Ваша оценка',
        widget=forms.TextInput(attrs={
            'class': 'form-control-plaintext',
            'value': '3',
            'readonly': True
        })
    )

    class Meta:
        model = BookReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите ваш отзыв...'
            })
        }


class ReaderProfileForm(forms.ModelForm):
    """Форма профиля читателя"""

    class Meta:
        model = Reader
        fields = ['phone', 'address', 'date_of_birth', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }


class BookIssueForm(forms.Form):
    """Форма выдачи книги"""
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(available_copies__gt=0),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )