from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post


def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Check passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
        username=username,
        email=email,
        password=password1
        )

        Profile.objects.create(user=user)


        messages.success(request, "Account created successfully!")
        return redirect("home")

    return render(request, "register.html")

def login_user(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request, "Login Successful!")

            return redirect("home")

        else:

            messages.error(request, "Invalid Username or Password")

            return redirect("login")

    return render(request, "login.html")

def logout_user(request):

    logout(request)

    messages.success(request, "Logged out successfully.")

    return redirect("home")

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    posts = Post.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total_posts = posts.count()

    total_likes = sum(
        post.likes.count() for post in posts
    )

    context = {
        "profile": profile,
        "posts": posts,
        "total_posts": total_posts,
        "total_likes": total_likes,
    }

    return render(
        request,
        "profile.html",
        context
    )

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        profile.bio = request.POST.get("bio")

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES.get("profile_picture")

        profile.save()

        return redirect("profile")

    return render(request, "edit_profile.html", {
        "profile": profile
    })

from django.contrib.auth.models import User

@login_required
def user_profile(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    profile, created = Profile.objects.get_or_create(
        user=user
    )

    posts = Post.objects.filter(
        user=user
    ).order_by("-created_at")

    total_posts = posts.count()

    total_likes = sum(
        post.likes.count() for post in posts
    )

    context = {

        "profile_user": user,

        "profile": profile,

        "posts": posts,

        "total_posts": total_posts,

        "total_likes": total_likes,

        "is_own_profile": request.user == user,
        
        "is_following": request.user in profile.followers.all(),

    }

    return render(
        request,
        "user_profile.html",
        context
    )

@login_required
def search_users(request):

    query = request.GET.get("q")

    users = User.objects.none()

    if query:

        users = User.objects.filter(
            username__icontains=query
        )

    return render(
        request,
        "search_results.html",
        {
            "query": query,
            "users": users
        }
    )

@login_required
def follow_user(request, username):

    target_user = get_object_or_404(
        User,
        username=username
    )

    if target_user == request.user:
        return redirect("user_profile", username=username)

    target_profile = Profile.objects.get(user=target_user)

    my_profile = Profile.objects.get(user=request.user)

    if request.user in target_profile.followers.all():

        target_profile.followers.remove(request.user)

        my_profile.following.remove(target_user)

    else:

        target_profile.followers.add(request.user)

        my_profile.following.add(target_user)

    return redirect(
        "user_profile",
        username=username
    )