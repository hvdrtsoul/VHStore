from django import forms
from .models import Movie, Equipment, Cassette
from .models import User as CustomUser
from django.contrib.auth.forms import UserCreationForm

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'release_year', 'image']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'price', 'description', 'image']

class CassetteForm(forms.ModelForm):
    movie = forms.ModelChoiceField(queryset=Movie.objects.all())  # Добавлено поле для выбора фильма

    class Meta:
        model = Cassette
        fields = ['movie', 'condition', 'price']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        #model = User this is the line that caused the error
        fields = ['username', 'email', 'password1', 'password2']