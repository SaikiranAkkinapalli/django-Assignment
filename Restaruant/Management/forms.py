from django.forms import ModelForm
from django import forms
from .models import UserModel, item,foodtype, table
import re
def check_phone_number(number):
    if len(number)>10:
        return False
    if not re.match("[6-9]{1}[0-9]{9}", number):
        return False
def number_check(number):
    if not re.match("[0-9]", number):
        return False
    return True
def price_check(number):
    if not re.match("[0-9][.][0-9]{2}", number):
        return False
    return True
def name_check(name):
    SpecialSym =['$', '@', '#', '%','!']
    val = True
    if any(char in SpecialSym for char in name):
        print('Password should have at least one of the symbols $@#')
        return False
    if val:
        return val
def password_check(passwd):
    SpecialSym =['$', '@', '#', '%','!']
    val = True
    if len(passwd) < 6:
        print('length should be at least 6')
        return False
    if len(passwd) > 20:
        return False
    if not any(char.isdigit() for char in passwd):
        return False
    if not any(char.isupper() for char in passwd):
        return False
    if not any(char.islower() for char in passwd):
        return False
    if not any(char in SpecialSym for char in passwd):
        return False
    if val:
        return val
class Additem(ModelForm):
    class Meta:
        model = item
        fields=['id','Name','Remaining','price','type']
    def clean_id(self):
        data=self.cleaned_data.get('id')
        if not number_check(data):
            raise forms.ValidationError('The Id Should be a number')
        return data
    def clean_Remaining(self):
        data=self.cleaned_data.get('Remaining')
        if not number_check(data):
            raise forms.ValidationError('The Remaining items should be a number')
        return data
    def clean_Remaining(self):
        data=self.cleaned_data.get('price')
        if not price_check(data):
            raise forms.ValidationError('The price should be a float')
        return data
    def clean_Name(self):
        data=self.cleaned_data.get('Name')
        if not name_check(data):
            raise forms.ValidationError('The Item Name Should not Contain Special Characters')
        return data
class AddFoodtype(ModelForm):
    class Meta:
        model=foodtype
        fields=['type']
    def clean_type(self):
        data=self.cleaned_data.get('type')
        if not name_check(data):
            raise forms.ValidationError('The Food Type Should not Contain Special Characters')
        return data
class AddTable(ModelForm):
    class Meta:
        model=table
        fields=['id','Seating_Capacity']
class CustomerForm(forms.Form):
    No_Of_People = forms.IntegerField(label='No.of People')
    def clean_Remaining(self):
        data=self.cleaned_data.get('No_Of_People')
        if not number_check(data):
            raise forms.ValidationError('The number of people should be number')
class SignUpForm(ModelForm):
    class Meta:
        model = UserModel
        fields=['first_name','last_name','Email','phonenumber','password']
        widgets = {
        'password': forms.PasswordInput(),
        'Email': forms.EmailInput(),
    }
    def clean_first_name(self):
        data=self.cleaned_data.get('first_name')
        if not name_check(data):
            raise forms.ValidationError('The First_Name Should not Contain Special Characters')
        return data
    def clean_last_name(self):
        data=self.cleaned_data.get('last_name')
        if not name_check(data):
            raise forms.ValidationError('The Last_Name Should not Contain Special Characters')
        return data
    def clean_phonenumber(self):
        data=self.cleaned_data.get('phonenumber')
        if not check_phone_number(data):
            raise forms.ValidationError('Enter Valid Phonenumber')
        return data
    def clean_password(self):
        data=self.cleaned_data.get('password')
        if not password_check(data):
            raise forms.ValidationError('The Password should have at least 1 uppercase,1lowercase,1special character')
        return data
class LoginForm(forms.Form):
    UserSign = forms.CharField(label='Email or Phone:',widget=forms.TextInput)
    password = forms.CharField(label='Password:', widget=forms.PasswordInput)

