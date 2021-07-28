from django.forms import ModelForm
from django import forms
from .models import UserModel, item,foodtype, table
class Additem(ModelForm):
    class Meta:
        model = item
        fields=['id','Name','Remaining','price','type']
class AddFoodtype(ModelForm):
    class Meta:
        model=foodtype
        fields=['type']
class AddTable(ModelForm):
    class Meta:
        model=table
        fields=['id','Seating_Capacity']
class CustomerForm(forms.Form):
    No_Of_People = forms.IntegerField(label='No.of People')
class SignUpForm(ModelForm):
    class Meta:
        model = UserModel
        fields=['first_name','last_name','Email','phonenumber','password']
        widgets = {
        'password': forms.PasswordInput(),
        'Email': forms.EmailInput(),
    }
class LoginForm(forms.Form):
    UserSign = forms.CharField(label='Email or Phone:',widget=forms.TextInput)
    password = forms.CharField(label='Password:', widget=forms.PasswordInput)

