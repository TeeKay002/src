from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateInput
from phonenumber_field.modelfields import PhoneNumberField
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    
    phone_number = PhoneNumberField(blank=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        # Hide help text for username and password fields
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
    

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=True)
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'gender']

        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }




    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('This phone number is already in use.')
        return phone_number



# accounts/forms.py
from django import forms
from .models import CustomGroup

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ['name']


