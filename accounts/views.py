from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #* imp 
# Create your views here.

def home(request):
    return render(request, 'home.html')


# !------------------------------------------------------------------------------------



# * Registration using -> Builtin User Model  (not required Models, ModelForm, Form)
# * Remember this is built in Model
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.password_validation import validate_password #* IMP
from django.core.exceptions import ValidationError  #* IMP

import string


def register_User_Model(request):

    # * NOTE = (that method does not required Models, ModelForm, Form) becuase here i am using built in Model User

    # Step-1 validation : Required fields
    if request.method == 'POST':

        name = request.POST.get('name' , "").strip() #* IMP
        password = request.POST.get('password',"").strip()
        confirm_password = request.POST.get('confirm_password',"").strip()
        # ('password',"") : Otherwise, if the key is missing, calling .strip() on None will raise an error.
        
        if not name:
            messages.error(request, "Name is required")
            return redirect('register_User_Model')
        if not password:
            messages.error(request, "Password is required")
            return redirect('register_User_Model')
        if not confirm_password:
            messages.error(request, "confirm_password is required")
            return redirect('register_User_Model')
        if password != confirm_password:
            messages.error(request, "password not matched")
            return redirect('register_User_Model')
        # if len(name) >= 20 or len(name) <= 3:
        #     messages.error(request, "Name should be greater than 3 and less than 20")
        #     return redirect('register_User_Model')
        
        # if not name.isalpha(): #* IMP : remember we can use directly
        #     messages.error(request, "Name must contains only alphabet characters")
        #     return redirect('register_User_Model')


    # Step-2 validation : Username already exists
        if User.objects.filter(username=name).exists(): #* IMP
            messages.error(request, "Username is already exist")
            return redirect('register_User_Model')

    # Step 3 — Password length
        # * validate_password will validate  #* IMP

        # if len(password) < 8:
        #     messages.error(request, "password should be at least 8 characters")
        #     return redirect('register_User_Model')

    # step-4 password validation
        # try:
        #     validate_password(password)
        # except ValidationError as e: #* imp
        #     messages.error(request, e.messages[0]) #* imp
        #     return redirect('register_User_Model')


    # step-4 manual validation
        # if not (
        #     any(c.isupper() for c in password) and
        #     any(c.islower() for c in password) and
        #     any(c.isnumeric() for c in password) and
        #     any(c in string.punctuation for c in password) 
        # ):

        # we can use helper function
            # messages.error(request, ' "Password should be mixed : One uppercase letter , One lowercase letter , One digit , One special character"')
            # return redirect('register_User_Model')
            
        # def checkpassword(value): # * imp : helping function
        #     return (
        #     any(c.isupper() for c in password) and
        #     any(c.islower() for c in password) and
        #     any(c.isnumeric() for c in password) and
        #     any(c in string.punctuation for c in password) 
        #     )
        # if not checkpassword(password):
        #     messages.error(request, ' "Password should be mixed : One uppercase letter , One lowercase letter , One digit , One special character"')
        #     return redirect('register_User_Model')

        # if not checkpassword(confirm_password):
        #     messages.error(request, ' "confirm Password should be mixed : One uppercase letter , One lowercase letter , One digit , One special character"')
        #     return redirect('register_User_Model')
        
        """ #* we can use loop also #imp
        for pwd in [password, confirm_password]:
            if not (
                any(c.isupper() for c in pwd) and
                any(c.islower() for c in pwd) and
                any(c.isdigit() for c in pwd) and
                any(c in string.punctuation for c in pwd)
            ):
                raise forms.ValidationError("Weak password")
        
        """
        
        # st = string.punctuation
        # check_special_char_inpass = any(i  in st for i in password)
        # check_alpha = any(i.isalpha() for i in password)
        # check_numeric = any(i.isnumeric() for i in password)
        # check_upper = any(i.isupper() for i in password)
        # check_lower = any(i.islower() for i in password)

        # complete = [check_numeric , check_alpha , check_special_char_inpass , check_upper , check_lower]
        # check = all(complete)

        # check_special_char_inname = any(i  in st for i in name)
        # if check_special_char_inname:
        #     messages.error(request, "Name must contains only alphabet characters")
        #     return redirect('register_User_Model')

    

        # if not check:
        #     messages.error(
        #         request, 
        #         "Password should be mixed : One uppercase letter , One lowercase letter , One digit , One special character"
        #         )
        #     return redirect('register_User_Model')

        try:
            User.objects.create_user( # in this view (user=User.objects.create_user) this is for Single-page approach,  when we will profile data create here in this view
                #  create_user() already creates and saves the user and returns a User instance, not a form. There is no form.save() after that.(❌ we can not so this user = User.objects.create_user()-> user.save())
                id , 
                username=name,
                password=password
                 # name = name, #* User have their own predifined fields so (❌ name) (✅ username.)
            )

            
        except Exception:
            messages.error(request, "Something went wrong. Please try again after sometime.")
            return redirect("register_User_Model")

        messages.success(request, 'registration successful using User Model')

        return redirect('user_login')
    
    return render(request, 'register_User_Model.html')


# !------------------------------------------------------------------------------------

# * Registration using -> UserCreationForm User Model  (not required Models, ModelForm, Form)
# * Remember this is built in Form

from django.contrib.auth.forms import UserCreationForm
def register_UserCreatioForm(request):
     
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save() # internally : user.set_password(raw_password) , : The user is the User model instance that the form creates.
            messages.success(request, "Registration successfully using UserCreatioForm")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register_UserCreatioForm.html', {'form':form})


# !------------------------------------------------------------------------------------

# * Registration usign Model form : now there is invlovements of Models(models.py), ModelForm(forms.py), 
from .forms import UserForm
def register_ModelForm(request):
    if request.method =="POST":
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Registration successfully using ModelForm")

            return redirect('home')

    else:
        form = UserForm()
    return render(request, 'register_ModelForm.html', {'form':form})



# !------------------------------------------------------------------------------------

# * Registration usign completely manually form : now there is invlovements of Models(models.py), ModelForm(forms.py), 
from .models import UserModel_manually
def register_manually(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')

        # manually validation parts (do it later)
        # -----
        # -----

        # save data in row and password is plain text not hashed right now
        UserModel_manually.objects.create(
            name=name,
            password=password
        )
        messages.success(request, "Registration successfully using manually")

        return redirect('home')
    return render(request, 'register_manually.html')



# !------------------------------------------------------------------------------------


# * for this registration i did not create html, url. it jsut for learning clean() and cleaned_data and super()
from .forms import Register_cleaned_data_form
def register_cleaned_data(request):

    if request.method == "POST":

        form = Register_cleaned_data_form(request.POST)
        
        """
        form
        ├── request.POST (raw data)
        └── cleaned_data = {}
        """

        if form.is_valid(): 
            # if form not valid
            # returns False, then
                # create_user() is not called.
                # cleaned_data should not be accessed.
                # Django stores validation errors in form.errors.
            """
            form
            ├── request.POST (raw data)
            ├── cleaned_data
            │   ├── username = "Anshul"
            │   └── password = "Password@123"
            │   └── confirm_password = "Password@123"
            └── errors = {}
            """

            username = form.cleaned_data['username'] #* imp : [] uses , this is used after form.is_valid()
            password = form.cleaned_data['password']
            try:
                User.objects.create_user( #* imp does not need request here
                    username=username,
                    password=password
                )
                return redirect('user_login')    
            except Exception: #* imp
                messages.error(request, "Server error")
                return redirect('register_cleaned_data')
    else:
        form =  Register_cleaned_data_form()
    return render(request, 'register_cleaned_data.html', {'form':form})



"""
Request
   │
   ├── POST?
   │      │
   │      ├── Yes
   │      │      │
   │      │      ├── form.is_valid() = True
   │      │      │      └── Create user → redirect
   │      │      │
   │      │      └── form.is_valid() = False
   │      │             └── return render(...)
   │      │
   │      └── No (GET)
   │             └── else → create empty form
   │
   └── return render(...)
"""









# !------------------------------------------------------------------------------------




# * Login with built in Authentication form does not required any other form


# * login 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , authenticate

# * used for traditional websites
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST) #* IMP
        
        if form.is_valid():
            user =  form.get_user()  #* imp
            login(request, user)

            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'user_login.html', {'form': form})


# !------------------------------------------------------------------------------------


# * mostly used 
def user_login_manual(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        
        user = authenticate(
            request, 
            username=username, 
            password=password
            )
        if user is not None:
            login(request, user)
            return redirect('content/profile')

    return render(request, 'user_login_manual.html')

"""
| Project Type                | Preferred Approach                                   |
| --------------------------- | ---------------------------------------------------- |
| Django HTML Templates       | ✅ `AuthenticationForm`                               |
| Django REST Framework (DRF) | ✅ Manual (`authenticate()` + `login()` or token/JWT) |
| React + Django              | ✅ Manual                                             |
| Flutter + Django            | ✅ Manual                                             |

"""




# user = form.save()          # ✅ Returns User object

# user = User.objects.create_user(...)   # ✅ Returns User object


# !------------------------------------------------------------------------------------
from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return redirect('home')


# !------------------------------------------------------------------------------------




# !------------------------------------------------------------------------------------

{ #* IMPORTANT
        # {user.set_password(...)   remaining to use}

    # * Specifically talking about (user creation / user registration / user signup).

    # * 1. for (user creation/user signup) built in Model(User) , and Built form(UserCreationForm) does not required to create Model class in model.py, form(it may be Form/ModelForm) class in forms.py

    # * 2. (create_user and set_password) is the methods of User model , can not use with model class like this:
            # ? UserModel.objects.create_user() ❌
            # ? RegisterModel.objects.create_user() ❌

            # | Model                                 | `create_user()` | `set_password()` |
            # | --------------------------------------| --------------- | ---------------- |
            # | Normal `models.Model`                 | ❌ No           | ❌ No            |
            # | Built-in `User`                       | ✅ Yes          | ✅ Yes           |
            # | Custom model                          | ✅ Yes          | ✅ Yes           |
            # |(`AbstractUser` / `AbstractBaseUser`)


    # * if you are using User model then , User model have their own predefined fields, can't craete custom :
    # ✅               ❌
    # username         name
    # password         user_password
    # first_name        
    # last_name     
    # email     
    # is_staff      
    # is_active     
    # date_joined       
    # last_login  
    
    # * User+create_user :
    # * Who creates the table? : Django's auth app.
    # * When you run: migrate, Django automatically creates tables such as:auth_user, auth_group etc....
    # * This is where User.objects.create_user() saves users.

    #     INSTALLED_APPS
    #         │
    #         ▼
    # django.contrib.auth
    #         │
    #         ▼
    # python manage.py migrate
    #         │
    #         ▼
    # Creates auth_user table automatically
    #         │
    #         ▼
    # User.objects.create_user(...)
    #         │
    #         ▼
    # Row inserted into auth_user


}


"""
Summary
    Normal UserModel + ModelForm + form.save() → Saves directly to your table.

    Built-in User + plain ModelForm + form.save() → Creates a user, but stores the password incorrectly unless you override the save logic.

    Built-in User + UserCreationForm or create_user() → Correct, secure way (password is hashed).



"""







"""



* you will use built-in User model + create_user + html form
* and UsercreationForm + is_valid + save() 


    | Your Approach                                                          | Used In                                              |  Production? | Table Where User Is Stored Notes                                                                                                                     |
    | ---------------------------------------------------------------------- | ---------------------------------------------------- | -----------: | -------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
    | **1. `User.objects.create_user()`**                                    | Custom registration page, API, custom business logic |        ✅ Yes | `auth_user`                | Very common. Password is 
    hashed automatically.                                                                            |

 *   | **2. `UserCreationForm`**                                              | Traditional Django websites (HTML templates)         |        ✅ Yes | `auth_user`                | Django's recommended registration form.                                                                                   |
 * (because) : The browser requests a page, Django renders HTML, and returns it. django -> browser-> HTML
 * todays The frontend and backend are separate.
 * React / Angular / Vue / Next.js
 *            ↓
 *      REST API / GraphQL
 *            ↓
 *          Django (DRF)
| Project Type                        | Common Approach                               |
| ----------------------------------- | --------------------------------------------- |
| Traditional Django (HTML templates) | ✅ `UserCreationForm`                          |
| Django + DRF API                    | ✅ `create_user()` inside a serializer/service |
| React + Django                      | ✅ `create_user()`                             |
| Flutter + Django                    | ✅ `create_user()`                             |
| Mobile App + Django                 | ✅ `create_user()`                             |

 

    | **3. `ModelForm` + `UserModel`**                                       | Learning, or custom non-auth models                  | ⚠️ Sometimes | Your `UserModel` table     | Only production if it's **not** the authentication user. If it's for authentication, you must hash the password yourself. |

    | **4. Manual (`request.POST` + `UserModel_manually.objects.create()`)** | Learning, testing                                    |         ❌ No | `UserModel_manually` table | Stores plain-text password, no validation, not connected to Django authentication.                                        |



    | Scenario                                           | Production Choice                                                           | Why                                                |
    | -------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------  |
    | Normal user registration (website/app)             | ✅ `UserCreationForm` (or a customized version)                              | Secure, validates passwords, hashes automatically |
*   | Custom registration page with extra fields         | ✅ Custom `UserCreationForm` (or) custom `Form` + `User.objects.create_user()` | Most common approach in production              |
    | API registration (DRF, mobile app, React, Flutter) | ✅ Serializer + `User.objects.create_user()`                                 | Forms aren't used in APIs                         |
    | Admin creates users                                | ✅ Django Admin                                                              | Already built-in                                  |
    | Custom user model (`AbstractUser`)                 | ✅ Custom `UserCreationForm` or `create_user()`                              | Standard Django approach                          |
    | Plain `ModelForm` + `User` model                   | ❌ Not used directly                                                         | Saves plain-text password unless you override it  |
    | Manual `request.POST` + `User.objects.create()`    | ❌ Not used                                                                  | No validation, password not hashed                |
    | Manual model (`UserModel_manually`)                | ❌ Not used                                                                  | Doesn't integrate with Django authentication      |













! nacessary validation 
You typically add checks like:

✅ Request method is POST.
✅ Username is not empty.
✅ Password is not empty.
✅ Confirm password matches.
✅ Username doesn't already exist.
✅ Email doesn't already exist (if using email).
✅ Handle database errors with try/except.
✅ Display success/error messages.



| Validation                 |   `UserCreationForm`  | You |
| ---------------------------| :-------------------: | :-: |
| Username required          |           ✅           |  ❌  |
| Username unique            |           ✅           |  ❌  |
| Password required          |           ✅           |  ❌  |
| Confirm password           |           ✅           |  ❌  |
| Password hashing           |           ✅           |  ❌  |
| Minimum length             |           ✅           |  ❌  |
| Common password            |           ✅           |  ❌  |
| Numeric-only password      |           ✅           |  ❌  |
| Password similarity        |           ✅           |  ❌  |
| Username format            |           ❌           |  ✅  |
| Username length (custom)   |           ❌           |  ✅  |
| Email validation           | ❌ (unless you add it) |  ✅  |
| mix Password               |           ❌           |  ✅  |
| Terms & Conditions         |           ❌           |  ✅  |
| CAPTCHA                    |           ❌           |  ✅  |


✅ Already handled by UserCreationForm
    ✅ Username is required.
    ✅ Username uniqueness.
    ✅ Password is required.
    ✅ Confirm password (password1 vs password2).
    ✅ Password minimum length.
    ✅ Password is not too common.
    ✅ Password is not entirely numeric.
    ✅ Password is not too similar to the username or other user attributes.
    ✅ Password hashing (set_password()).


Your manual validation checks:

✅ Minimum length (you wrote this separately).
✅ At least one uppercase letter.
✅ At least one lowercase letter.
✅ At least one digit.
✅ At least one special character.

So yes, it enforces a mixed/strong password.

However, Django's validate_password() does more (depending on your AUTH_PASSWORD_VALIDATORS settings).

It can also check:

✅ Minimum length.
✅ Password isn't too similar to the username or other user attributes.
✅ Password isn't a common password (e.g., password123, qwerty123).
✅ Password isn't entirely numeric (e.g., 12345678).
✅ Any custom validators you've added.
"""
