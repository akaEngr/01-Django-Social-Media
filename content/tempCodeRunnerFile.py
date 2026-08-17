mport ProfileForm
# def user_profile(request):

#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES)
        
#         if form.is_valid():

#             name = form.cleaned_data['name']
#             age = form.cleaned_data['age']
#             bio = form.cleaned_data['bio']
#             profile_photo = form.cleaned_data['profile_photo']
            
#             ProfileModel.objects.create(
#                 user = request.user,
#                 name=name,
#                 age=age,
#                 bio=bio,
#                 profile_photo = profile_photo
#             )
#             messages.success(request, "Profile created succussfully")
#             return redirect('user_profile')
#     else:
#         form = ProfileForm()
#     return render(request, 'user_profile.html', {'form':form,})


# from .forms import PostForm
# from .models import TagModel