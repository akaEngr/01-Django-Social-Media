from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

from .forms import ProfileForm
def user_profile(request):

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        
        if form.is_valid():

            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            bio = form.cleaned_data['bio']
            profile_photo = form.cleaned_data['profile_photo']
            
            ProfileModel.objects.create(
                user = request.user,
                name=name,
                age=age,
                bio=bio,
                profile_photo = profile_photo
            )
            
            messages.success(request, "Profile created succussfully")
            return redirect('user_profile')
    else:
        form = ProfileForm()
    return render(request, 'user_profile.html', {'form':form,})


from .forms import PostForm
from .models import TagModel


def user_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
             
        if form.is_valid():
            post_text = form.cleaned_data['post_text']
            tag_text = form.cleaned_data['tag_text']
            
            # * remember here we are dealing to separate input , beucase each input goes to separate table , that's why need to store input separately one by one. #imp
            # * fisrt table
            post = PostModel.objects.create(   #* imp : we store speparate post data, and need to get object and send in post local variable
                    post_text = post_text,
                    profile = request.user.profilemodel,
                )
            
            split_tags = tag_text.replace(",","").split()

            # you are just adding tag name to tag_text which is a separte table (your TagModel) you are connecting tag to post here
            for i in split_tags:
                tag,created = TagModel.objects.get_or_create(   #* imp store speparate tag data
                        tag_text = i
                    )
                # (tag,created) tag is variable here 
                # This is where Django connects both objects.
                post.tag.add(tag)
                # post : <PostModel id=1 post_text="Learning Django">
                # tag : <TagModel id=2 tag_text="python">
                
                """
                Connect 
                Post ID = 1 
                with 
                Tag ID = 2                                                          
                
                post_id   tag_id
                -----------------
                1         2

                """

            messages.success(request, "Post created succussfully")

            return redirect('user_post')
    else:
        form = PostForm()
    return render(request, 'user_post.html', {'form':form})


from .models import PostModel, ProfileModel
def showdata_profile_post(request):

    profile_all_data = ProfileModel.objects.all() # it use for only send all deta for selct and option when we use iterate ovver this all data
    post_all_data = PostModel.objects.all() # it use for only send all deta for selct and option when we use iterate ovver this all data
    filtered_profile_data = None
    filtered_post_data = None
   

    seleted_profile_id = request.GET.get('profile_dropdown')
    seleted_post_id = request.GET.get('post_dropdown')
    # backward approach
    if seleted_profile_id:
        choose_profile = ProfileModel.objects.get(id=seleted_profile_id)
        filtered_post_data = choose_profile.postmodel_set.all() #* impt : i write post , but it should be model name which is postmodel
        # <ModelName in lowercase>_set
    # forward approach
    if seleted_post_id:
            choose_post = PostModel.objects.get(id=seleted_post_id)
            filtered_profile_data = choose_post.profile

            """
            | Relationship      | Forward          | Backward                      |
            | ----------------- | ---------------- | ----------------------------- |
            | **ForeignKey**    | `post.profile`   | `profile.postmodel_set.all()` |
            | **OneToOneField** | `profile.user`   | `user.profilemodel`           |
            | **ManyToMany**    | `post.tag.all()` | `tag.postmodel_set.all()`     |

            """
    context = {
        'seleted_post_id': seleted_post_id,
        'seleted_profile_id': seleted_profile_id,
        'profile_all_data': profile_all_data,
        'post_all_data': post_all_data,
        'filtered_profile_data': filtered_profile_data,
        'filtered_post_data' : filtered_post_data
    }
    
    return render(request, 'showdata_profile_post.html', context)



def showdata_post_tags(request):
    # fisrtly we need to get all data based on fields that are connected to relationship means post and tags

    post_all_data = PostModel.objects.all()
    tag_all_data = TagModel.objects.all()

    select_post_id = request.GET.get('select_post_id')
    select_tag_id = request.GET.get('select_tag_id')

    filtered_post_data = None
    filtered_tag_data = None

    if select_post_id:
        choose_post = PostModel.objects.get(id=select_post_id)
        filtered_tag_data = choose_post.tag.all()

    if select_tag_id:
        choose_tag = TagModel.objects.get(id=select_tag_id)
        filtered_post_data = choose_tag.postmodel_set.all()

    context = {
        'filtered_post_data': filtered_post_data,
        'filtered_tag_data' : filtered_tag_data,
        'post_all_data' : post_all_data,
        'tag_all_data' : tag_all_data,
        'select_post_id': select_post_id,
        'select_tag_id' : select_tag_id
    }

    return render(request, 'showdata_post_tags.html', context)
    
# from django.shortcuts import get_object_or_404
# def show_post_likes(request):
#     post_all_data = PostModel.objects.all()
#     post_id = request.POST.get('post_id')
#     post = get_object_or_404(PostModel, id=post_id)
#     post.like.add(request.user)
        
#     return render(request, 'show_post_likes.html', {'post_all_data':post_all_data})
from django.shortcuts import get_object_or_404

# @login_required
# def show_post_likes(request):

#     post_all_data = PostModel.objects.all()

#     if request.method == "POST":

#         post_id = request.POST.get("post_id")

#         post = get_object_or_404(PostModel, id=post_id)

#         user = request.user
#         # toggle like/unlike
#         if user in post.like.all():
#             post.like.remove(user)
#             messages.info(request, "You unliked the post")
#         else:
#             post.like.add(user)
#             messages.success(request, "You liked the post")

#         # redirect to avoid double POST and refresh displayed data
#         return redirect(request.path)

#     return render(
#         request,
#         "show_post_likes.html",
#         {"post_all_data": post_all_data}
#     )



from .models import CommentModel
@login_required
def show_post_comment(request):

    post_all_data = PostModel.objects.all()

    if request.method == "POST":
        user = request.user

        if 'post_comment_id' in request.POST:
            post_comment = request.POST.get('post_comment')


            post_comment_id = request.POST.get("post_comment_id")

            post_comment_object = get_object_or_404(PostModel, id=post_comment_id)

            CommentModel.objects.create(
            comment_text = post_comment,
            post = post_comment_object,
            user = user,
            )
            
            messages.success(request, "You commented on the post")
            return redirect('show_post_comment')


        elif "post_like_id" in request.POST:

            post_like_id = request.POST.get("post_like_id")
            post_like_object = get_object_or_404(PostModel, id=post_like_id)

        
        # toggle like/unlike
            if user in post_like_object.like.all():
                post_like_object.like.remove(user)
            else:
                post_like_object.like.add(user)

            messages.success(request, "You liked the post")

        # redirect to avoid double POST and refresh displayed data
            return redirect('show_post_comment')

    return render(
        request,
        "show_post_comment.html",
        {"post_all_data": post_all_data}
    )














def methodspractice(request):
    print("|----------------------------------|")
    print("|---------------START--------------|")
    print("|----------------------------------|")
    print()

    # ?-------------------------------------------------------------------------
    # ! 1. Retrieving Data

    # ! 1. Model.objects.all()

    # We have those models
    # 1. PostModel
    # 2. CommentModel
    # 3. ProfileModel
    # 4. TagModel
    print("HY")
    # * 1. PostModel.objects.all
    print("-------\n| 1. PostMode.objects.all() \n-------\n")

    all_post_data = PostModel.objects.all()     

     # Postmodel contians and connected with Regular Fields and Relationship Fields
     # 1. profile
     # 2. tag
     # 3. like
     # 4. commentmodel
     # 5. user (get go though other field path )
    Post_number = 0
    print("1. PostModel -> post_text (Forward approach)\n")
    if all_post_data:
        print("-> All User Post text data")
        
        for post in all_post_data:
            Post_number+=1
            print()
            print()
            print("| ----------------------------")
            print("| Post Number : ", Post_number)
            print("| ----------------------------")
            print("| Post text : ", post.post_text)
            print("| Post id :   ", post.id)
            print("|")
            
            # 2. PostModel->tag (Forward approach)
            for post_tag_data in post.tag.all():
                # post.tag.all() contains all the query set of all tag data for a partiucar , and post_tag_data will iterate on each query and return an obejct
                print(f"| Post tag :    {post_tag_data.tag_text}")
                print(f"| Post tag id : {post_tag_data.id}")
                print("|")

                # now go thorugh path -> deeper ralations access
                print("|",post_tag_data.tag_text,"tag is used for those posts : ")
                for get_post_from_tag in post_tag_data.postmodel_set.all():

                    # post_tag_data.postmodel_set.all() contains all the post for a particual tag
                    print("| Post text->",get_post_from_tag)
                print("|")
            # 2. PostModel->like (Forward approach)
            for post_liked_by in post.like.all():
                print("| Post Liked By : ", post_liked_by)
                print("|")
                print("| This User Also liked those posts")
                for get_post_based_on_like in post_liked_by.profilemodel.postmodel_set.all():
                    print("|",get_post_based_on_like.post_text)
                #     print("-------------")
                print("|")
            # 3. PostModel->commentmodel (reverse approach)
            for commented_by in post.commentmodel_set.all():
                # ! IMP : to get user comments then post.comment_text is thier comments and who commented in this then do comment.user, why comment.user work becuase user is field of the commentmodel
                print("| Post Comment : ", commented_by.comment_text)
                print("| Post Commented By : ", commented_by.user)
                print("| Post Commented on post : ", commented_by.post.post_text)
                print("| Post id : ", commented_by.post.id)
                print("| Post user name : ", commented_by.post.profile.user)
                print("|")

                # now go deeper get back to posts commented by this user
                # * comments - posts
                print(f"| Get posts back of user {commented_by.user}")  
                for get_posts in commented_by.user.profilemodel.postmodel_set.all():
                    print("|",get_posts.post_text)

                # * user - comments
                print(f"| Get comment back of user {commented_by.user}")  
                for get_posts in commented_by.user.profilemodel.postmodel_set.all():
                    print("|",get_posts.post_text)

            print("|")
            print("| Post Profile : ", post.profile) # it will return an object # subh_profile : because of __str__, self.name (means profile.name)
            print("| Post name : ", post.profile.name)
            print("| Post profile id : ", post.profile.id)
            print("| Post Profile user : ", post.profile.user)
            print("| Post Profile user id : ", post.profile.user.id)

            
            

    print("-----------------------------------")
    print("Total Post ", all_post_data.count())
    print("-----------------------------------")
    print("----End of PostModel.object.all()----")
    print()
    print("|----------------------------------|")
    print("|----------------END---------------|")
    print("|----------------------------------|")
    print()
    print()
    print("|------------------------------------------------------------------------|")
    print()




# ! ----------------------------------------------------------------------------------------------------------------------
# ! ----------------------------------------------------------------------------------------------------------------------
# !   ------------------------ .get() ------------------------
# ! ----------------------------------------------------------------------------------------------------------------------
# ! ----------------------------------------------------------------------------------------------------------------------


  
    print("|----------------------------------|")
    print("|---------------START--------------|")
    print("|----------------------------------|")
    print()

    print("-------\n| 1. TagModel.objects.get() \n-------\n")
    # get return a single object and can get error if field not found

    tag = TagModel.objects.get(tag_text = "Python")
    print("| Object    :",tag)
    print("| tag text  :",tag.tag_text)
    print("| tag id    :",tag.id)   
    # we can get relavent fields
    for get_posts in tag.postmodel_set.all():
        print("|")
        print("| object    :",get_posts)
        print("| post id   :",get_posts.id)
        print("| post text :",get_posts.post_text)
    
    # now we will get object using differnt keys
    # get return single object so what we can get : thorugh id (mostcommonly used) from the forntenf we get id then get object based on that.
    # # Don't use get() if this lookup can return multiple objects.
    tag1 = TagModel.objects.get(tag_text = "Python")
    tag2 = TagModel.objects.get(id = 23)
    # ! Use get() when the query is guaranteed to return exactly one object.
    # * Otherwise : ❌ Raises MultipleObjectsReturned.
    # tag__id :
    # ❌ But get() must return exactly one object. If multiple objects match (e.g., many posts have the same tag), it raises MultipleObjectsReturned.
    print(f"| \n| {tag1} \n| {tag2}")


    # let's take id form the html page

    all_tag_data = TagModel.objects.all()

    get_tag_id = request.GET.get('tag_id') #* imp

    get_post_obj = PostModel.objects.filter(tag__id = get_tag_id)



    print()
    print()
    print()
    print("|----------------------------------|")
    print("|----------------END---------------|")
    print("|----------------------------------|")



# ! ----------------------------------------------------------------------------------------------------------------------
# ! ----------------------------------------------------------------------------------------------------------------------
# !   ------------------------ .filter() ------------------------
# ! ----------------------------------------------------------------------------------------------------------------------
# ! ----------------------------------------------------------------------------------------------------------------------




    print("|----------------------------------|")
    print("|---------------START--------------|")
    print("|----------------------------------|")
    print()


    print("-------\n| 1. .filter() \n-------\n")

    # postmodel
    # ! imp : filter always return queryset
    filter_id = PostModel.objects.filter(id = 55)
    filter_post_text = PostModel.objects.filter(post_text = 'post 2 by Anshul')
    filter_tag = PostModel.objects.filter(tag__id = '22')
    filter_tag = PostModel.objects.filter(tag__id = '22')    

    print(f"| \n| {filter_id} \n| {filter_post_text} \n")




    print("-------\n| 1. .exclude() \n-------\n")
    for all_p in all_post_data:
        print(all_p.id)
    print() # having id 59
    query_exclude = PostModel.objects.exclude(id = 59)
    query_first = PostModel.objects.first()
    query_last = PostModel.objects.last()

    print(query_first)
    print(query_last)
    for p in query_exclude:
        print(p.id) # it does not have



    a = PostModel.objects.order_by('post_text')
    for x in a:
        print(x)    
    print()
    a = PostModel.objects.order_by('-id')
    for x in a:
        print(x)    


    print("---")
    print("---")
#     a = PostModel.objects.order_by(
#     "-id",
#     "post_text"
# ) # imp never work for two conditions


# ------------------------------------------------------

    print("-------\n| .count() \n-------\n")

    a = all_post_data.count()
    print("Total posts :", a)
    a = all_tag_data.count()
    print("Total tags :", a)
    

    print()

#! ------------------------------------------------------

    print("-------\n| .exists() \n-------\n")

    a = PostModel.objects.filter(id = 55).exists()
    print(a) # True





    print()

#! ------------------------------------------------------

    print("-------\n| __contains \n-------\n")
    print()

    a_x = PostModel.objects.filter(tag__tag_text__contains = 'PYthon')
    for x in a_x:
        print(x) # 


#! ------------------------------------------------------


    print()
    print("-------\n| __startswith \n-------\n")

    a_x = PostModel.objects.filter(tag__tag_text__startswith = 'thon')
    for x in a_x:
        print(x) # nohting showing 








#! ------------------------------------------------------


    print()
    print("-------\n| __gt \n-------\n")

    a_x = ProfileModel.objects.filter(age__gt = 10)
    for x in a_x:
        print(x) # nohting showing 

#! ------------------------------------------------------


    print()
    print("-------\n| __gtes \n-------\n")

    a_x = ProfileModel.objects.filter(age__gte = 10)
    for x in a_x:
        print(x) # nohting showing 



#! ------------------------------------------------------


    print()
    print("-------\n| __in \n-------\n")
    # means get posts that matches

    a_x = ProfileModel.objects.filter(age__in = [10])
    for x in a_x:
        print(x) 




#! ------------------------------------------------------
# ! IMP : when you need specific field of data : Use .values() ----------------------------------------------------------------
# ! all :  gives completed data
# ! return dictionory

    print()
    print("-------\n| .values() \n-------\n")
    # means get posts that matches

    a_values = ProfileModel.objects.values('name', 'age')
    print(a_values)
    print()
    print()

    for value in a_values:
        print(f"{value['name']} : {value['age']}")

    print()
    print()
    for profile in a_values:
        for key, value in profile.items():
            print(key, value)

    # ! this will not work
    # for name,age in a_values:
    #     print(f"{a_values[0]}")
    #     print(f"{a_values[1]}")

 


# #! ------------------------------------------------------
#     # same as vlaues , but return tuple
    
    print()
    print("-------\n| .values_list() \n-------\n")
    # means get posts that matches

    a_values_list = ProfileModel.objects.values_list('name', 'age')
    print(a_values_list)
    print()

    for name,age in a_values_list:
        print(name, age)

    # other way

    print()
    print()
    for profile in a_values_list:
        print(name, age)




# #! ------------------------------------------------------
#     # same as vlaues , but return tuple
    
    print()
    print("-------\n| .a_values_distinct() \n-------\n")
    # avoid dupliicates

    a_values_distinct = ProfileModel.objects.distinct()
    print(a_values_distinct)


    a_values_distinct = ProfileModel.objects.values('name').distinct()
    print(a_values_distinct)





# #! ------------------------------------------------------
    
    print()
    print("-------\n| Imp info () \n-------\n")


    PostModel.objects.filter(profile=request.user.profilemodel)
    # it will gives you post of current logged in user
    # when you create socialmedia app and in profile wants to show logged in posts then it will need it

    PostModel.objects.filter(tag__tag_text="python")

    CommentModel.objects.filter(post=post)
    # post (left) → CommentModel's ForeignKey field.
    # ! post (right) → a Post object stored in the Python variable post. (post = Post.objects.get(id=5))
    # ! imp : here we are passing complete object to post foregin key field : so it auto rxtract it. and we can give object to field

    PostModel.objects.filter(like=request.user)





  

# #! ------------------------------------------------------
    
    print()
    print("-------\n| Imp () \n-------\n")

    range_posts = ProfileModel.objects.filter(age__range = [10,12])
    print(range_posts)

    """
    | Lookup    | Works On                                                 |
    | --------- | -------------------------------------------------------- |
    | `__year`  | `DateField`, `DateTimeField` only                        |
    | `__month` | `DateField`, `DateTimeField` only                        |
    | `__day`   | `DateField`, `DateTimeField` only                        |
    | `__range` | Dates, numbers, IDs, prices, and other comparable fields |


    Rule to Remember
    __year, __month, __day → Date/Time fields only.
    __range → Any field where "between A and B" makes sense.
    """
   
    # Post.objects.filter(created_at__range=["2026-01-01", "2026-01-31"])
    # Post.objects.filter(created_at__year=2026)
    # Post.objects.filter(updated_at__month=7)
    # Post.objects.filter(birth_date__day=17)






#! ------------------------------------------------------
    from django.db.models import Count , Sum, Avg, Max, Min
    print()
    print("-------\n| Aggregation () \n-------\n")
    
    print("-------\n| Count() :  \n-------")
    # Count # Sum # Avg # Min # Max
    count__total_age = ProfileModel.objects.aggregate(total_age = Count('age'))
    print(count__total_age)

    count__total_age = ProfileModel.objects.aggregate(total_name = Count('name'))
    print(count__total_age)
    
    count__total_age = PostModel.objects.aggregate(total_like = Count('like'))
    print(count__total_age)

    count__total_age = CommentModel.objects.aggregate(total__comment = Count('comment_text'))
    print(count__total_age)
    print()


# !------------------------------------------------------

    print("-------\n| Sum() :  \n-------")
    Sum_age = ProfileModel.objects.aggregate(total_age = Sum('age'))
    print(Sum_age)
    print()

# !------------------------------------------------------

    print("-------\n| Avg() :  \n-------")
    Avg_age = ProfileModel.objects.aggregate(Avg_age = Avg('age'))
    print(Avg_age)
    print()

# !------------------------------------------------------

    print("-------\n| MAX() :  \n-------")
    Max_age = ProfileModel.objects.aggregate(Max_age = Max('age'))
    print(Max_age)
    print()


# !------------------------------------------------------

    print("-------\n| MIN() :  \n-------")
    Min_age = ProfileModel.objects.aggregate(Min_age = Min('age'))
    print(Min_age)
    print()


# !------------------------------------------------------

    from django.db.models.functions import Random

    print("-------\n| Random() :  \n-------")

    # ! Random can be used throgh order_by

    Random_Post = PostModel.objects.all().order_by(Random())
    for post in Random_Post:
        print(post)
    


    print()


# !------------------------------------------------------

    print("-------\n| related_name :\n-------")
    """
    Interview Definition
        related_name is used to give a custom name to the reverse relationship instead of Django's default <modelname>_set. It makes the code more readable and meaningful. 
    """

    # profile.postmodel_set.all()
    # Without related_name

    # With related_name

    # class PostModel(models.Model):
    #     profile = models.ForeignKey(
    #         ProfileModel,
    #         on_delete=models.CASCADE,
    #         related_name='posts'
    #     )

    # Now use:
    # profile.posts.all()


# !------------------------------------------------------

    print("-------\n| through() :  \n-------")

    """
    * PostTag Model (insted of creating hidden table)
    class PostTag(models.Model):
        post = models.ForeignKey(PostModel, on_delete=models.CASCADE)

        tag = models.ForeignKey(TagModel, on_delete=models.CASCADE)

        added_by = models.ForeignKey(User, on_delete=models.CASCADE)

        added_at = models.DateTimeField(auto_now_add=True)


    * PostModel (you previous postmodel with adding through) 
    class PostModel(models.Model):
    post_text = models.CharField(max_length=100)

    tag = models.ManyToManyField(
        TagModel,
        through="PostTag"
    )

    for i in split_tags:
    tag, created = TagModel.objects.get_or_create(
        tag_text=i
    )

    PostTag.objects.create(
        post=post,
        tag=tag,
        added_by=request.user,
    )

    ! Only this line changed : : post.tag.add(tag)

    * PostModel table
        | id | post_text       |
        | -- | --------------- |
        | 1  | Learning Django |
        | 2  | Python Tips     |

    * TagModel
        | id | tag_text |
        | -- | -------- |
        | 1  | Python   |
        | 2  | Django   |
        | 3  | Backend  |

    * PostTag (YOUR table)
        | post_id | tag_id | added_by | added_at |
        | ------- | ------ | -------- | -------- |
        | 1       | 1      | Ansh     | 10-Jul   |
        | 1       | 2      | Rahul    | 11-Jul   |
        | 2       | 1      | Ansh     | 12-Jul   |

    --------------------------------------------
    * Without through
        Post
          │
          ▼
        Tag
       
        Hidden Table
       
        | post_id | tag_id |

    * With through
        Post
         │
         ▼
        Tag

        Your Table

        | post_id | tag_id | added_by | added_at |
        


    * Simple Definition (Best for learning)
    ? through is used to replace Django's hidden Many-to-Many table with our own model, so we can store extra fields in the relationship.
    """
    

    


    # ! imp : .add() : post.tag.add(tag) we do when relationship we used M2M

    from .models  import FollowModel

    all_profile_user = ProfileModel.objects.exclude(user=request.user)
    print(all_profile_user)
    if request.method == "POST":
        user = request.user

        get_following_id = request.POST.get("profile_id")
        if get_following_id:
            get_profile_obj = ProfileModel.objects.get(id=get_following_id)

            follow_obj , created = FollowModel.objects.get_or_create(
            follower = user,
            following = get_profile_obj.user,
        )


        get_unfollow_id = request.POST.get("unfollow_id")
        if get_unfollow_id:
            get_profile_obj_for_unfollow = ProfileModel.objects.get(id=get_unfollow_id)

            
            FollowModel.objects.filter(
                follower = user,
                following = get_profile_obj_for_unfollow.user,
            ).delete()

            print("Deleted")

        # ! we can also directly do : FollowModel.objects.get_or_create
        

   
    get_user_following = FollowModel.objects.filter(follower = request.user).count()     
    print(get_user_following)

    get_user_followers = FollowModel.objects.filter(following = request.user).count()     
    print(get_user_followers)

    profile = request.user.profilemodel

    total_followers_count = profile.total_followers
    print(total_followers_count)

    total_following_count = profile.total_following
    print(total_following_count)






# !-----------------------------


    print("-------\n| related_name :\n-------")

    post = ProfileModel.objects.annotate(total_post = Count('postmodel'))
    for p in post:
        print(p.name, p.total_post)
    print()

    
    profile = ProfileModel.objects.all()
    for profile in profile:
        total_post = profile.postmodel_set.count()
        print(profile.name, total_post)









    print()
    print()
    print()
    print("|----------------------------------|")
    print("|----------------END---------------|")
    print("|----------------------------------|")







 
    context = {
        'all_post_data' : all_post_data,
        'all_tag_data' : all_tag_data,
        'get_post_obj' : get_post_obj,
        'a_values' : a_values,
        'all_profile_user' : all_profile_user,
    }

    return render(request, 'methodspractice.html', context)


































"""


| Method                | If no data found   | Use                                              |
| --------------------- | ------------------ | ------------------------------------------------ |
| `get()`               | ❌ Raises exception | `try...except`                                   |
| `get_object_or_404()` | ❌ Raises `Http404` | Usually no `try` in views (let Django handle it) |
| `first()`             | `None`             | `if`                                             |
| `last()`              | `None`             | `if`                                             |
| `filter()`            | Empty `QuerySet`   | `if` or `.exists()`                              |
| `all()`               | Empty `QuerySet`   | `if` or `.exists()`                              |
| `exclude()`           | Empty `QuerySet`   | `if` or `.exists()`                              |
| `values()`            | Empty `QuerySet`   | `if` or `.exists()`                              |
| `values_list()`       | Empty `QuerySet`   | `if` or `.exists()`                              |



"""











"""
| Query                         | Returns                                    | Return Type                      |
| ----------------------------- | ------------------------------------------ | -------------------------------- |
| `Model.objects.all()`         | All matching records                       | **QuerySet**                     |
| `Model.objects.filter()`      | Matching records                           | **QuerySet**                     |
| `Model.objects.exclude()`     | Non-matching records                       | **QuerySet**                     |
| `Model.objects.get()`         | Exactly one record                         | **Single Model Object**          |
| `Model.objects.first()`       | First record or `None`                     | **Single Model Object / `None`** |
| `Model.objects.last()`        | Last record or `None`                      | **Single Model Object / `None`** |
| `Model.objects.count()`       | Total number of records                    | **Integer (`int`)**              |
| `Model.objects.exists()`      | Whether records exist                      | **Boolean (`True`/`False`)**     |
| `Model.objects.values()`      | Dictionaries of selected fields            | **QuerySet**                     |
| `Model.objects.values_list()` | Tuples (or single values with `flat=True`) | **QuerySet**                     |
| `Model.objects.order_by()`    | Ordered records                            | **QuerySet**                     |
| `Model.objects.distinct()`    | Unique records                             | **QuerySet**                     |
| `Model.objects.none()`        | Empty result                               | **QuerySet**                     |


"""