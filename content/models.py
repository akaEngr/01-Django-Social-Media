from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileModel(models.Model):
    name = models.CharField(max_length=20) #* imp
    age = models.IntegerField()
    bio = models.CharField(max_length=100)

    profile_photo = models.ImageField(
        upload_to = 'profile_photos/',
        # What is upload_to? : It tells Django-> "Inside the MEDIA folder, where should this file be stored?"
        blank=True,
        null=True
    )

    # here we added one-to-one relationship
    # when ever you use o2o relationship then it will not allow to create multiple so so 1 user - 1 profile
    # user is inside the profile , profile belongs to user
    user  = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,
        null=True,)


    # ! property # imp ---------------------------------------------------
    @property
    def total_followers(self):
        return FollowModel.objects.filter(
            following = self.user
        ).count()

    @property
    def total_following(self):
        return FollowModel.objects.filter(
            follower = self.user
        ).count()
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
    



    
class TagModel(models.Model):
    tag_text = models.CharField(max_length=100, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.tag_text


# ! NOTE : whatever fields inside post model their fields will be show in post table
# !---------------------------------------------

# ! Custom queries

class PostManager(models.Manager):

    def published(self):
        return self.filter(status = "published")
"""
models.Manager
it already has methods like:

filter()
all()
get()
exclude()

That's why you can write:




PostModel.objects.published()

PostModel
     │
     ▼
objects
     │
     ▼
PostManager()
     │
     ▼
published()
     │
     ▼
self.filter(status="published")
     │
     ▼
QuerySet
"""    


"""
| id | post_text | status    |
| -- | --------- | --------- |
| 1  | Django    | published |
| 2  | Python    | draft     |
| 3  | AI        | published |
posts = PostModel.objects.published()
print(posts)

<QuerySet [
    <PostModel: Django>,
    <PostModel: AI>
]>
"""

class PostModel(models.Model):
    post_text = models.CharField(max_length=20) #* imp

    profile = models.ForeignKey(
        ProfileModel, 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        )
    
    like = models.ManyToManyField(User, blank=True)
    
    tag = models.ManyToManyField(TagModel)
    
    status = models.CharField(max_length=20, default="Draft")

    objects = PostManager()
    class Meta:
        ordering = ['id']

    def __str__(self): # it expect string only when you do slef.profile then it will show error becuase profile is contains id
        return self.post_text




class CommentModel(models.Model):
    comment_text = models.CharField(max_length=100)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # One User  ─────► Many Comments
    # One Post  ─────► Many Comments





# class FollowModel(models.Model):
#     following = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         )


#     followers  = models.ForeignKey(
#         User, on_delete=models.CASCADE
#         )
# ! imp : Django will raise an error because both reverse relationships would try to use the same default name:
# user.followmodel_set 
# User ← followmodel_set
# User ← followmodel_set
# ❌ Conflict! Which one should user.followmodel_set represent?


class FollowModel(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    

# ! imp : why we needed to use related name in that followmodel.
# first understand relationship
# there are two foreignkey relationship with same User Model.

# without related name we will perform reverse relationship like : 
# *user.followmodel_set.all
# * follower ?
# * following ?
# this is the class followmodel inside it follower and following now think where it is refrencing ???????:
# for those field (those field are separate ) but we have to use same syntax which make conflict
# so required related name 
# now see changes
# * user.follower.all
# * user.following.all

# *user.followmodel_set.all
# * follower ?
# * following ?

# * A Many-to-Many relationship is physically implemented using an intermediate (junction) table that contains two ForeignKeys.

# ! The key concept
# ! Each row = one follow relationship.
# Two ForeignKeys do not automatically mean a Many-to-Many relationship.

# They become a Many-to-Many because the model is acting as a junction (bridge) between two entities.

# A junction table doesn't store a list.
# It stores one connection per row.







"""
| Query                                              | Need `__`? | Why?                                               |
| -------------------------------------------------- | ---------- | -------------------------------------------------- |
| `PostModel.objects.filter(post_text="Python")`     | ❌ No       | `post_text` is in `PostModel`.                     |
| `PostModel.objects.filter(profile=profile_obj)`    | ❌ No       | You're filtering on the relationship field itself. |
| `PostModel.objects.filter(profile_id=1)`           | ❌ No       | You're using the foreign key ID shortcut.          |
| `PostModel.objects.filter(profile__name="Anshul")` | ✅ Yes      | `name` is in `ProfileModel`.                       |
| `PostModel.objects.filter(tag__id=2)`              | ✅ Yes      | `id` is in `TagModel`.                             |
| `PostModel.objects.filter(tag__tag_text="django")` | ✅ Yes      | `tag_text` is in `TagModel`.                       |

"""