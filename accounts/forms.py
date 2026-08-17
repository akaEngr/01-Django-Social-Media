from django import forms
from .models import  UserModel
import string

# ! imp about save : save() is commonly used when you already have a model object.

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = '__all__'


class Register_cleaned_data_form(forms.Form): 
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=20)
    confirm_password = forms.CharField(max_length=20)
    # Simple difference:
        # Form (forms.Form) → Validate data → You save to the database manually.
        # ModelForm (forms.ModelForm) → Validate data + Can save directly using form.save().  

    # Django always performs its built-in validation first. Only if it passes does Django call your clean_<field>(). If your manual validation also passes, the returned value is stored in form.cleaned_data.

    
    def clean_username(self):
        username = self.cleaned_data['username']
        """
        [] means:
            "I am 100% sure this key exists."
            If the key does not exist, Python raises:
        """

        if not username.isalpha() or username.istitle():
      
            raise forms.ValidationError(
                "Only tital case allowed"
            )
        return username

    def clean_password(self):
        password = self.cleaned_data['password'] #* imp []
        
        st = string.punctuation
        if not(
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isalpha() for c in password) and
            any(c.isnumeric() for c in password) and
            any(c in st for c in  password) 
        ):
            raise forms.validationError(
                "password should contains at least one uppercase and one lowercase and one special character and one numeric"
            )
    
        return password
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']

        st = string.punctuation
        if not(
            any(c.isupper() for c in confirm_password) and
            any(c.islower() for c in confirm_password) and
            any(c.isalpha() for c in confirm_password) and
            any(c.isnumeric() for c in confirm_password) and
            any(c in st for c in  confirm_password) 
        ):
            raise forms.ValidationError(
                "confirm password should contains at least one uppercase and one lowercase and one special character and one numeric"
            )
    
        return confirm_password

    def clean(self):
        cleaned_data = super().clean() #* imp   
        # means:
        # "Call the parent class's clean() method and get the cleaned_data dictionary so I can perform my own cross-field validation."
        # It says:
        # "Django, give me the final cleaned data after all field validations are complete."      

        # super() : "Go to my parent (base) class." , : class RegisterForm(forms.Form):

        # clean() : The parent class forms.Form has a built-in clean() method that returns the current cleaned_data dictionary after Django has finished the individual field validations.

        password = cleaned_data.get('password') #* imp .get()
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password do not match"
            )
        return cleaned_data

        # This tells Django:
        # "Everything is valid. Keep this cleaned data."


"""

Rule
✅ clean_<field>() → Use forms.ValidationError
✅ clean() (multiple fields together) → Use forms.ValidationError
✅ views.py (success/failure after processing) → Use messages

Remember:

Inside Forms → ValidationError
Inside Views → messages
"""















"""






"""


"""
Difference between Form and ModelForm in Django

Form:
- Used for validation only.
- Fields are created manually.
- Database saving is handled manually.

ModelForm:
- Connected with a model.
- Fields are created automatically from the model.
- Handles model validation.
- Can save data using form.save().

from django import forms
from django.db import models
from django.contrib.auth.models import User


# =========================
# MODEL
# =========================

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()


# =========================
# 1. NORMAL FORM
# =========================

class ProductForm(forms.Form):
    Normal Form:
    - We manually define fields.
    - Django only validates data.
    - We manually save data.

    name = forms.CharField(max_length=100)
    price = forms.IntegerField()


# views.py example with Form

def add_product_using_form(request):

    form = ProductForm(request.POST)

    if form.is_valid():

        # cleaned_data contains validated data
        name = form.cleaned_data["name"]
        price = form.cleaned_data["price"]

        # Manual database saving
        Product.objects.create(
            name=name,
            price=price
        )


# =========================
# 2. MODEL FORM
# =========================

class ProductModelForm(forms.ModelForm):
    ModelForm:
    - Connected with Product model.
    - Automatically creates fields.
    - Performs model validation.
    - Provides save() method.

    class Meta:
        model = Product
        fields = "__all__"


# views.py example with ModelForm

def add_product_using_modelform(request):

    form = ProductModelForm(request.POST)

    if form.is_valid():

        # Automatically creates Product object
        form.save()


# =========================
# EXTRA FIELD IN MODELFORM
# =========================

class RegisterModelForm(forms.ModelForm):

    # This field does not exist in User model
    confirm_password = forms.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )

        return cleaned_data


# =========================
# USER REGISTRATION COMPARISON
# =========================


# Manual Registration using Form:

Form
 |
 |-- Validate username/password/confirm_password
 |
 |-- User.objects.create_user()
 |
 Database


# Using UserCreationForm:


UserCreationForm (ModelForm)
 |
 |-- Built-in validation
 |-- Password matching
 |-- Password validation
 |
 |-- form.save()
 |
 Database


# =========================
# SUMMARY
# =========================

Form:
    - Manual fields
    - Validation
    - No save()
    - Manual database operations

ModelForm:
    - Model connected
    - Automatic fields
    - Model validation
    - form.save()
    - Create/update model objects

User Model:
    - Database table
    - Can work with Form, ModelForm, or UserCreationForm
"""