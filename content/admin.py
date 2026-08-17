from django.contrib import admin
from .models import FollowModel, ProfileModel, PostModel, CommentModel, TagModel
# Register your models here.
# admin.site.register(CommentModel)
# admin.site.register(FollowModel)

@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','name','age','bio', 'profile_photo' ,'user_id_display') # some of  those are field names define in models

    def user_id_display(self, obj):
        return obj.user.id if obj.user else "-"
    user_id_display.short_description = "User ID"



@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','tag_text')

@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','post_text','profile_id_display','liked_user_ids' , 'show_tags') #* imp (comma is imp,)


    def show_tags(self, obj):
        return ", ".join(tag.tag_text for tag in obj.tag.all())

  
    def profile_id_display(self, obj):
        return obj.profile.id if obj.profile else "-"
    profile_id_display.short_description = "Profile ID"

    def liked_user_ids(self, obj):
        return ", ".join(str(user.id) for user in obj.like.all()) or "-"
    liked_user_ids.short_description = "Liked User IDs"

  # older version
    # def profile_id(self, obj):
    #    return obj.profile.id if obj.profile else '-'
   
       
    # profile_id.short_description = "profile_id"


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','comment_text','user_id_display','post_id_display') #* imp (comma is imp,)

    def user_id_display(self, obj):
        return obj.user.id if obj.user else '-'
    user_id_display.short_description = "USER ID"

    def post_id_display(self, obj):
        return obj.post.id if obj.post else '-'
    post_id_display.short_description = "POST ID"





@admin.register(FollowModel)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower_id' , 'following_id')













