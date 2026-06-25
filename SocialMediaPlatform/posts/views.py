from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST


from .models import Post

def home(request):

    posts = Post.objects.all().order_by("-created_at")

    return render(request, "home.html", {"posts": posts})


@login_required
def create_post(request):

    if request.method == "POST":

        content = request.POST["content"]

        image = request.FILES.get("image")

        Post.objects.create(
            user=request.user,
            content=content,
            image=image
        )

        return redirect("home")

    return render(request, "create_post.html")

@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    if request.method == "POST":
        post.delete()

    return redirect("profile")

@login_required
def edit_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    if request.method == "POST":

        post.content = request.POST.get("content")

        if request.FILES.get("image"):
            post.image = request.FILES.get("image")

        post.save()
        messages.success(
    request,
    "Post updated successfully."
    )

        return redirect("profile")

    return render(
        request,
        "edit_post.html",
        {
            "post": post
        }
    )

@login_required
@require_POST
def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():

        post.likes.remove(request.user)

        liked = False

    else:

        post.likes.add(request.user)

        liked = True

    return JsonResponse({

        "liked": liked,

        "likes": post.likes.count()

    })

from django.http import JsonResponse

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        text = request.POST.get("text")

        if text.strip():

            comment = Comment.objects.create(

                post=post,

                user=request.user,

                text=text

            )

            return JsonResponse({

                "username": comment.user.username,

                "text": comment.text,

                "created": comment.created_at.strftime("%d %b %Y")

            })

    return JsonResponse({"error": "Invalid request"})