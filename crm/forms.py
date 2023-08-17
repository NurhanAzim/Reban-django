from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, EmailValidator
from django.db.models import Sum
from django import forms
from .models import Egg, Chicken, EggShipment
import datetime

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

    size0 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Saiz', 'value':'Kecil', 'readonly': 'True'}))
    quantity0 = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Kuantiti', 'min':'0'}), validators=[MinValueValidator(0)], required=False)
    size1 = forms.CharField( label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Saiz', 'value':'Sederhana', 'readonly': 'True'}))
    quantity1 = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Kuantiti', 'min':'0'}), validators=[MinValueValidator(0)], required=False)
    size2 = forms.CharField( label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Saiz', 'value':'Besar', 'readonly': 'True'}))
    quantity2 = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Kuantiti', 'min':'0'}), validators=[MinValueValidator(0)], required=False)

    class Meta:
        model = Egg
        fields = [] 

    def clean(self):
        cleaned_data = super().clean()

        # Get the quantity fields and their values
        quantity_fields = ['quantity0', 'quantity1', 'quantity2']
        quantity_values = [cleaned_data.get(field, 0) for field in quantity_fields]

        # Check if any quantity field has a value greater than 0
        has_non_zero_quantity = any(value and value > 0 for value in quantity_values)

        if has_non_zero_quantity:
            # Set the quantity of other fields to 0 if they are not filled
            for field in quantity_fields:
                if cleaned_data.get(field) is None:
                    cleaned_data[field] = 0
        else:
            # If no quantity field has a value greater than 0, allow any combination of blank and zero values
            for field in quantity_fields:
                if cleaned_data.get(field) is None:
                    cleaned_data[field] = 0

        return cleaned_data

class AddChickenForm(forms.ModelForm):

    date_added = forms.DateField(label="", widget=DateInput(attrs={'class': 'form-control', 'placeholder': 'Tarikh ditambah'}))
    age = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Umur (Minggu)'}), validators=[MinValueValidator(1)], help_text='<span class="form-text text-muted"><small>Umur ayam dalam minggu <strong>(semasa tarikh ditambah)</strong>.</small></span>')
    health_status = forms.ChoiceField(label="", choices=Chicken.HEALTH_STATUS_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'placeholder': 'Status kesihatan'}))
    purpose = forms.ChoiceField(label="", choices=Chicken.PURPOSE_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Tujuan'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.date.today()
        self.fields['date_added'].widget.attrs['max'] = today.strftime('%Y-%m-%d')

    class Meta:
        model = Chicken
        exclude = ['owner']
        
class AddShipmentForm(forms.ModelForm):
    date_shipped = forms.DateField(label="", widget=DateInput(attrs={'class':'form-control', 'placeholder':'Tarikh dihantar'}))
    customer = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nama pelanggan'}), max_length=100)
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ulasan', 'rows':3}), max_length=300, required=False)
    eggs_quantity = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Kuantiti telur (dozen)', 'min':0}), validators=[MinValueValidator(1)])
    is_mixed_size = forms.BooleanField(label="Campur saiz", widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':'is_mixed_size', 'placeholder':'Campur saiz'}), required=False, initial=False)
    size = forms.ChoiceField(label="", choices=Egg.EGG_SIZE_CHOICES, widget=forms.Select(attrs={'class':'form-control','id':'size', 'placeholder':'Saiz'}), required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get accumulated egg quantity from the logged-in user's eggs
        accumulated_quantity = Egg.objects.filter(owner=user).exclude(egg_shipment__isnull=False).count()
        max_dozens = accumulated_quantity // 12
        if max_dozens > 0:
            self.fields['eggs_quantity'].widget.attrs['max'] = max_dozens
            self.fields['eggs_quantity'].help_text = '<span class="form-text text-muted"><small>Anda mempunyai {} dozen telur dalam stok.</small></span>'.format(max_dozens)
        else:
            self.fields['eggs_quantity'].widget.attrs['max'] = 0
            self.fields['eggs_quantity'].help_text = '<span class="form-text text-muted"><small>Anda tidak mempunyai telur mencukupi dalam stok.</small></span>'
    
    class Meta:
        model = EggShipment
        exclude = ['eggs','owner']