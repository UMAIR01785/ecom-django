from django import forms
from . models import Account

class RegisterForm(forms.ModelForm):
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        max_length=20,
        required=True
    )
    confirm_password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        max_length=20,
        required=True
    )
    
    class Meta:
        model = Account
        fields=('first_name','last_name','email','username','phone_number','password')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email address'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose username'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter phone number'})


    