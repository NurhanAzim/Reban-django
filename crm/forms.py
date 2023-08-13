from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, EmailValidator
from django import forms
from .models import Egg, Chicken

class DateInput(forms.DateInput):
    input_type = 'date'

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'E-mel'}), validators=[EmailValidator], help_text='<span class="form-text text-muted"><small>Alamat emel yang sah.</small></span>')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nama Pengguna'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Maksimum 150 aksara. Hanya huruf, nombor dan @/./+/-/_ sahaja.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Kata Laluan'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Minima 8 aksara. Tidak boleh sama dengan Nama Pengguna.</small></span>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Sahkan Kata Laluan'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Masukkan kata laluan sekali lagi.</small></span>'

class AddEggForm(forms.ModelForm):

    size = forms.ChoiceField(choices=Egg.EGG_SIZE_CHOICES, label="", widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Saiz'}))
    quantity = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Kuantiti'}), validators=[MinValueValidator(1)])

    class Meta:
        model = Egg
        exclude = ['collection_date','owner']

class UpdateEggForm(forms.ModelForm):
    quantity = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form--control', 'placeholder':'Kuantiti'}), validators=[MinValueValidator(1)])

    class Meta:
        model = Egg
        exclude = ['collection_date','owner','size',]

class AddChickenForm(forms.ModelForm):

    date_added = forms.DateField(label="", widget=DateInput(attrs={'class': 'form-control', 'placeholder': 'Tarikh ditambah', 'max': '{{ today }}'}))
    age = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Umur (Minggu)'}), validators=[MinValueValidator(1)])
    health_status = forms.ChoiceField(label="", choices=Chicken.HEALTH_STATUS_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'placeholder': 'Status kesihatan'}))
    purpose = forms.ChoiceField(label="", choices=Chicken.PURPOSE_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Tujuan'}))

    class Meta:
        model = Chicken
        exclude = ['owner']
        