from django.db import models

# Create your models here.
# UserModel for register

# * model is just for create table in database , using this model if you create ModelForm then data will be add in table as row

# * f you try to manually store user data then still you need to use User model becuase create_user and set_password are the methods of User model (not any common model UserModel class) 

"""
| Model                                              | `create_user()` | `set_password()` |
| -------------------------------------------------- | --------------- | ---------------- |
| Normal `models.Model`                              | ❌ No            | ❌ No             |
| Built-in `User`                                    | ✅ Yes           | ✅ Yes            |
| Custom model (`AbstractUser` / `AbstractBaseUser`) | ✅ Yes           | ✅ Yes            |



Rule
Creating a user record → ModelForm ✅
Login → Form ✅
Change Password → Form ✅
Forgot Password / OTP → Form ✅
"""


# * this model i am using to implement with built in User model (this comes in middle means no completely manually not compeltely builtin)

class UserModel(models.Model):
    username = models.CharField(max_length=20)
    password = models.IntegerField()
    blank=True
    null=True
    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.username


class UserModel_manually(models.Model):
    name = models.CharField(max_length=20)
    password = models.IntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


