from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from datetime import datetime, timezone
from journeyapp.models import Triplog, Profile, Likes, Follow, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage

from django.conf import settings
import random

# Create your views here.

def index(request):
    
    return render(request, 'homepage.html')


def user_register(request):
    
    if request.method == "GET":
        
        return render(request, 'register.html')
    
    else:
        
        username = request.POST['username']
        
        request.session['username'] = username
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            
            u = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)
            
            u.set_password(password)
            
            u.save()
            
            return redirect('/profilepic')
        
        else:
            
            context = {}
            
            context['error'] = "Password and Confirm Password does not match"
            
            return render(request, 'register.html', context)
        
        
def user_login(request):
    
    
    
    if request.method == "GET":
        
        return render(request, 'login.html')
    
    
    else:
        
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            login(request, user)
            
            return redirect('/')
        
        else:
            
            context = {}
            
            context["error"] = "Username and Password is Incorrect"
            
            return render(request, 'login.html', context)
        
def user_logout(request):
    
    logout(request)
    
    return redirect('/')




def profilepic(request):
    if request.method == "GET":
        return render(request, 'profilepic.html')
    else:
        Username = request.session.get('username')
        print(Username)
        user = User.objects.get(username = Username)
        
        if user:
        
            bio = request.POST['bio']
            profile_pic = request.FILES['profile_pic']
            location = request.POST['location']
            birth_date = request.POST['birth_date']
            
            p = Profile.objects.create(
                bio=bio,
                profile_pic=profile_pic,
                location=location,
                birth_date=birth_date,
                user = user
            )
            
            p.save()

            return redirect('/login')
        
        else:
            return redirect('/register')
        



@login_required(login_url="/login")        
def create_log(request):
    
    if request.method == "GET":
        
        return render(request, 'trip.html')
    
    else:
        
        user = request.user
        image = request.FILES['image']
        caption = request.POST['caption']
        
        
        if image:
            
            t = Triplog.objects.create(user = user, caption = caption, image = image)
            
            t.save()
            return redirect('/')
        
        else:
            
            context = {}
            
            context["error"] = "Image is reqired to create post"
            
            return render(request, 'trip.html', context)


def profile_view(request):
    # Get the currently logged-in user
    user = request.user
    
    # Retrieve the user's profile or return a 404 if it doesn't exist
    profile = get_object_or_404(Profile, user=user)
    pro = Profile.objects.filter(user = user)
    
    # t = Triplog.objects.filter(user = user)
    
    posts = Triplog.objects.filter(user=user).order_by('-created_at')
    
    
    context = {}
    
    context['profile'] = profile
    context['posts'] = posts
    context['pro'] = pro
    # context["data"] = t
    
    # Pass the profile to the template
    return render(request, 'read_profile.html', context)



def update_profile(request, rid):
    
    if request.method == "GET":
        
        p = Profile.objects.filter(id = rid)
        
        context = {}
        
        context['data'] = p
        
        return render(request, 'updateprofile.html', context)
    
    else:
        
        bio = request.POST['bio']
        
        location = request.POST['location']
        birth_date = request.POST['birth_date']
            
        p = Profile.objects.filter(id = rid)
        
        p.update(bio = bio, location = location, birth_date = birth_date)
        
        return redirect('/profile')

def read_log(request):
    
    posts = Triplog.objects.all().exclude(user = request.user).order_by('-created_at')
    
    
    
    
    context = {}
    
    context['data'] = posts
    
    return render(request, 'read_post.html', context)

def update_log(request,rid):
    if request.method == 'GET':
        p = Triplog.objects.filter(id = rid)
        context = {}
        context['data'] = p
        return render(request,'update_post.html',context)
    else:
        caption = request.POST['caption']
        p = Triplog.objects.filter(id = rid)
        p.update(caption = caption, updated_at = datetime.now())
        return redirect('/read_log')

def triplog_detail(request, rid):
    
    p = Profile.objects.filter(id = rid)
    
    log = Triplog.objects.filter(id = rid)     #use for to send in html
    
    l = Triplog.objects.get(id = rid)
    
    com = Comment.objects.filter(triplog = l).order_by('-created_at')
    
    
    
    context = {}
    
    context['data'] = log
    
    context['profile'] = p
    
    context['comment'] = com
    
    if request.method == "GET":
            
        return render(request, "triplog_detail.html", context)
        
    else:
            
        comments = request.POST['comments']
            
        t = Triplog.objects.get(id = rid)
            
        c = Comment.objects.create(triplog = t, user = request.user, comments = comments)
            
        c.save()
            
        

        return render(request, 'triplog_detail.html', context)


def like_count(request, Log_id):
    
    username = User.objects.get(username =request.user.username)
    post = Triplog.objects.get(id = Log_id)
    
    
    
    like_filter = Likes.objects.filter(Log_id=post, username=username).first()
    
    if like_filter is None:
        new_like = Likes.objects.create(Log_id=post, username=request.user)
        post.like_count += 1
        new_like.save()
        
    else:
        like_filter.delete()
        post.like_count -= 1
    
    post.save()
    return redirect('/read_log')

def show_users(request):
    
    # user = User.objects.all()
    
    p = Profile.objects.all().exclude(user = request.user)
    
    context = {}
    
    context['data'] = p
    
    return render(request, 'show_users.html',context)


def detail_users(request, rid):
    
    p = Profile.objects.get(id = rid)
    profile = Profile.objects.filter(id = rid)
    
   
    # Get the currently logged-in user
    user = User.objects.get(username = request.user.username)
    
    
    follower = Follow.objects.filter(follower=p.user)               #The result is stored in followers, representing all users who follow the profile's user.
    following = Follow.objects.filter(following=p.user)             #The result is stored in following, representing all users that the profile's user is following.
    
    user_has_followed = Follow.objects.filter(follower=user, following=p.user).exists()
    
    print(user_has_followed)
    
    context = {
                        'data': profile,
                        'following': follower,
                        'followers': following,
                        'user_has_followed': user_has_followed
                        }
    
    
    # Pass the profile to the template
    
    return render(request, 'detail_user.html',context)


@login_required(login_url="/login") 
def follow_user(request,rid):
    user_follow = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(id = rid)
    follow_relation = Follow.objects.filter(follower=user_follow, following = profile.user).first()
    
    
    if follow_relation is None:
        Follow.objects.create(following = profile.user, follower = user_follow)
        profile.followers_no += 1
        profile.save()
        
        
        
        user_profile = Profile.objects.get(user = user_follow)
        user_profile.folllowings_no += 1
        user_profile.save()
    
    else:
        follow_relation.delete()
        
        profile.followers_no -= 1
        profile.save()
        
        user_profile = Profile.objects.get(user = user_follow)
        user_profile.folllowings_no -= 1
        user_profile.save()
    
    
    return redirect(f'/detail_users/'+ rid)

# def create_comments(request, rid):
    
#     if request.method == "GET":
            
#             return render(request, "triplog_detail.html")
        
#     else:
            
#         comments = request.POST['comments']
            
#         t = Triplog.objects.get(id = rid)
            
#         c = Comment.objects.create(triplog = t, user = request.user, comments = comments)
            
#         c.save()
            
#         return HttpResponse("Commented")
    
    
    
def forgot_password(request):
    
    if request.method == "GET":
        
        return render(request, "forgot_password.html")
    
    else:
        
        email = request.POST['email']
        
        request.session['email'] = email
        
        user = User.objects.filter(email = email).exists()
        
        if user:
        
            otp = random.randint(1000, 9999)
            
            request.session['otp'] = otp
            
            with get_connection(
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                user_tls = settings.EMAIL_USE_TLS
            ) as connection :
                
                subject = "OTP Verification"
                email_from = settings.EMAIL_HOST_USER
                reciption_list = [email]
                message = f"OTP is {otp}"
                
                EmailMessage(subject, message, email_from, reciption_list, connection = connection).send()
            return redirect('/otp_verification')
        
        else:
            
            context = {}
            
            context['error'] = "User Not a Found"
            
            return render(request, 'forgot_password.html', context)
        
    
def otp_verification(request):
    
    if request.method == "GET":
        
        return render(request, 'otp.html')
    
    else:
        
        otp = int(request.POST['otp'])
        
        email_otp = int(request.session['otp'])
        
        if otp == email_otp:
            
            return redirect("/new_password")
        
        else:
            
            context = {}
            
            context['error'] = "OTP does not match"
            
            return render(request, 'forgot_password.html', context)
        
        
def new_password(request):
    
    if request.method == "GET":
        
        return render(request, 'new_password.html')
    
    else:
        
        email = request.session['email']
        
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        user = User.objects.get(email = email)
        
        if password == confirm_password:
            
            user.set_password(password)
            
            user.save()
            
            return redirect("/login")
        
        else:
            
            context ={}
            
            context['error'] = "Password and confirm Password does not match"
            
            return render(request, 'new_password.html', context)
        
        
def delete_log(request, rid):
    
    trip = Triplog.objects.filter(id = rid)
    
    trip.delete()
    
    return redirect("/profile")

def show_detail_post(request, rid):
    p = Profile.objects.filter(id = rid)
    
    log = Triplog.objects.filter(id = rid)     #use for to send in html
    
    l = Triplog.objects.get(id = rid)
    
    com = Comment.objects.filter(triplog = l).order_by('-created_at')
    
    
    
    context = {}
    
    context['data'] = log
    
    context['profile'] = p
    
    context['comment'] = com
    
    if request.method == "GET":
            
        return render(request, "show_detail_post.html", context)
        
    else:
            
        comments = request.POST['comments']
            
        t = Triplog.objects.get(id = rid)
            
        c = Comment.objects.create(triplog = t, user = request.user, comments = comments)
            
        c.save()
            
        

        return render(request, 'show_detail_post.html', context)