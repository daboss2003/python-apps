
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
import json
from .models import User,Post,Notification,Comment,Like,Profile,Friend
from django.core.paginator import Paginator
from django.db.models import Q


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"status":"CSRF cookie set"})


@login_required
def index(request):
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
            posts = Post.objects.all()
            posts = posts.order_by("-timestamp").all()
            friend_requests = Friend.objects.filter(friend=request.user,is_accepted=False)
            if friend_requests:
                friend_count = friend_requests.count()
            else:
                friend_count = " "
            notifications =  Notification.objects.filter(user=request.user,is_read=False)
            if notifications:
                notification_count = notifications.count()
            else:
                notification_count = " "
            
            paginator = Paginator(posts,10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "network/index.html",
             {"page_obj" :page_obj,
              "friend_count":friend_count,"notification_count":notification_count
              }           
        )
        else:
            return HttpResponseRedirect(reverse("edit_profile"))
    else:
        return HttpResponseRedirect(reverse('login'))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def get_profile(request,user_id):
    if request.method == 'GET':
        user = get_object_or_404(User,pk=user_id)
        profile = Profile.objects.filter(user=user)
        friend = Friend.objects.filter(user=user) 
        user_friend = []
        for j in friend:
            if request.user.id == j.friend.id:
                user_friend.append(j.friend)
            elif request.user.id == j.user.id:
                user_friend.append(j.friend)
        posts = Post.objects.filter(user=user)
        posts = posts.order_by("-timestamp").all()
        friends = Friend.objects.filter(friend=user)
        paginator = Paginator(posts,10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request,"network/profile.html",{
            "profiles":profile,
            "page_obj":page_obj,
            "friends":friends,
            "user_friend":user_friend
        })
    elif request.method == 'POST':
        user = get_object_or_404(User,pk=user_id)
        if Profile.objects.filter(user=user).exists():
            user_profile = get_object_or_404(Profile,user=user_id)
            user_bio = request.POST.get('user_bio')
            user_pics = request.FILES.get('user_pics')
            user_profile.bio = user_bio
            user_profile.profile_picture = user_pics
            user_profile.save()
        else:
            user_bio = request.POST.get('user_bio')
            user_pics = request.FILES.get('user_pics')
            profile = Profile.objects.create(user=request.user,bio=user_bio,profile_picture=user_pics)
            profile.save()
        messages.add_message(request,messages.SUCCESS,"profile created successfully")
        return HttpResponseRedirect(reverse("index"))
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)


@login_required
def create_user_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        type = request.POST.get('media_type')
        media = request.FILES.get("media")
        new_post = Post.objects.create(user=request.user,content=content,media=media,media_type=type)
        new_post.save()
        messages.add_message(request,messages.SUCCESS,"post created successfully")
        return HttpResponseRedirect(reverse("index"))
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)

            
        

@login_required 
def edit_post(request,post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=post_id)
        content = request.POST.get("content")
        media = request.FILES.get("media")
        type = request.POST.get("media_type")
        post.content = content
        post.media = media
        post.media_type = type
        post.user = request.user
        post.save()
        messages.add_message(request,messages.SUCCESS,"post updated successfully")
        return HttpResponseRedirect(f"/get_post/{post_id}")
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)

            



@login_required      
def get_friends_post(request):
    if request.method == 'GET':
        user = request.user
        friends = Friend.objects.filter(Q(user=user) | Q(friend=user))
        friend = []
        if friends:     
            for i in friends:
                friend_list =  Post.objects.filter(Q(user=i.friend)| Q(user=i.user))
                for j in friend_list:
                    friend.append(j.user.id)
        else:
            friend = None
        if friend != None:
            posts = Post.objects.filter(user__in=friend).exclude(user=user)
            posts = posts.order_by("-timestamp").all()
        else:
            posts = Post.objects.filter(user=friend)
        paginator = Paginator(posts,10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request,"network/friend_post.html",{
            'page_obj':page_obj
        })
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)
        


@login_required
def get_post(request,post_id):
    if request.method == 'GET':
        posts = get_object_or_404(Post,pk=post_id)
        return render(request,"network/post.html",{
            "post":posts
        })
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)


@login_required
def get_like(request,post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=post_id)
        user = request.user
        if Like.objects.filter(post=post,user=user).exists():
            Like.objects.filter(post=post,user=user).delete()
            like_count = Like.objects.filter(post=post).count()
        else:
            likes = Like.objects.create(post=post,user=user,is_like=True)
            likes.save()
            like_count = Like.objects.filter(post=post).count()
        return  JsonResponse({"like_count":like_count}, safe=False)
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)
    


@login_required
def get_comment(request,post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=post_id)
        content = request.POST.get("comment")
        if content == "":
            messages.add_message(request,messages.INFO,"failed")
            return HttpResponseRedirect(f"/get_post/{post_id}")
        else:
            comment = Comment.objects.create(content=content,user=request.user,post=post)
            comment.save()
            text = f"{request.user} Comment to Your Post"
            new_notification = Notification.objects.create(user=request.user,post=post,type="post",content=text)
            new_notification.save()
            messages.add_message(request,messages.SUCCESS,"Comment Placed Successfully")
        return render(request,"network/post.html",{
            "post":post
        })
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)
    




@login_required
def get_notification(request):
    if request.method == "GET":
        user = request.user
        notifications = Notification.objects.filter(user=user,is_read=False)
        notifications.order_by("-timestamp").all()
        return render(request,"network/notification.html",{"notification":notifications})
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        notifications_id = data.get("id")
        notifications = get_object_or_404(Notification,pk=int(notifications_id))
        notifications.is_read = True
        notifications.save()
        return JsonResponse({"success":"done"})
    
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)
    
        
        




def get_all_user(request):
    if request.method == "GET":  
        friend_requests = Friend.objects.filter(friend=request.user,is_accepted=False)
        friends = Friend.objects.filter(Q(user=request.user) | Q(friend=request.user))
        friend = []
        if friends:
           for p in friends:
               friend.append(p.user)
               friend.append(p.friend)
               
        else:
            friend = None
        if friend == None:
            users = Profile.objects.all().exclude(user=request.user)
        else:
            users = Profile.objects.all().exclude(user=request.user).exclude(user__in=friend)
        return render(request,"network/follow_request.html",{
            "people":users,
            "friend_requests" : friend_requests})
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)
    

@login_required  
def send_friend_request(request,friend_id):
    if request.method == "GET":
        friend = get_object_or_404(User,pk=friend_id)
        if Friend.objects.filter(user=request.user,friend=friend).exists() or request.user == friend:
            Friend.objects.filter(user=request.user,friend=friend).delete()
            return JsonResponse({"response":"not_ok"},safe=False)
        else:
             new_friend = Friend.objects.create(user=request.user,friend=friend)
             new_friend.save()
             text = f"{request.user.username} Started Following You"
             new_notification = Notification.objects.create(user=friend,content=text)
             new_notification.save() 
             return JsonResponse({"response":"ok"})
    if request.method == "POST":
        decision1 = request.POST.get("accept")
        decition2 = request.POST.get("delete")
        friend = get_object_or_404(User,pk=friend_id)
        if decision1:
            new_friend = get_object_or_404(Friend,friend=request.user,user=friend)
            new_friend.is_accepted = True
            text = f"{request.user.username} Whom you follow now follows You"
            new_friend.save()
            new_notification = Notification.objects.create(user=friend,content=text)
            new_notification.save()
        else:
            Friend.objects.filter(friend=request.user,user=friend).delete()
        return HttpResponseRedirect(reverse("get_all_user"))
    else:
        return JsonResponse({'status':'error',"message":"Method not allowed"},status=405)
    


def edit_profile(request):
    return render(request,"network/edit_profile.html")
    
        


        