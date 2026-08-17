from django import forms
from .models import ProfileModel, PostModel

# modelform is connected to the database but form not
# ModelForm is preferred because it stays synchronized with the model, uses model validation, supports both create and update easily, and reduces the chance of manual mapping errors—not just because it saves lines of code.


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        # fields = '__all__'
        fields = ['name', 'age', 'bio','profile_photo']

class PostForm(forms.ModelForm):
    # *imp
    # here we explicitly included tag text beacuse by default form is giving select and option and we want only input . 
    tag_text =  forms.CharField(max_length=100,required=False, help_text='Separate tags with spaces')


    
    class Meta:
        model = PostModel
        fields = ['post_text',] #* imp
        # * becuase we separately used tag_text so can not wrote __all__
        # here we did not used profile because profile is connected with user so we can directly give : profile = request.user.profilemodel
        
# def liked_user_ids(self, obj):
#         return ", ".join(str(user.id) for user in obj.like.all()) or "-"
#     liked_user_ids.short_description = "Liked User IDs"

# tell me one thing what happend if create separate model for like , comment, or without model direct using relation field inside post .

