from django import forms
from . models import Accounts

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control small-input',
        'placeholder':'Entre the password',
    }), max_length=50, required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control small-input',
        'placeholder':'Entre the password',
    }), max_length=50, required=True)

    class Meta:
        model= Accounts
        fields=['first_name','last_name','email','phone_number','password']

    def __init__(self,*args,**kwargs):
         super(RegisterForm,self).__init__(*args,**kwargs)
         self.fields['first_name'].widget.attrs['placeholder']='Entre the First name'
         self.fields['last_name'].widget.attrs['placeholder']='Entre the last name'
         self.fields['email'].widget.attrs['placeholder']='Entre the Email'
         self.fields['phone_number'].widget.attrs['placeholder']='Entre the Phone number'
         for item in self.fields:
             self.fields[item].widget.attrs['class']='form-control'

    def clean(self):
        clean_data=super(RegisterForm,self).clean()
        password=clean_data.get('password')
        confirm_password=clean_data.get('confirm_password')

        if password != confirm_password:
            raise ValueError("The password should be match ")
        
