
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post 


def scratch(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 2)

    if request.GET.get("page"):
        page_number = request.GET.get("page")
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    return render(request, "network/scratch.html", {"page_obj": page_obj})


def index(request):
    if request.user.is_authenticated:
        return render(request, "network/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
def follow(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Username not found."}, status=404)

    if request.method != "PUT":
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


    data = json.loads(request.body)
    requestor = User.objects.get(username=request.user)
    if requestor in user.followers.all() and data['follow'] is False:
        user.followers.remove(requestor)
        requestor.following.remove(user)
    if requestor not in user.followers.all() and data['follow'] is True:
        user.followers.add(requestor)
        requestor.following.add(user)

    return HttpResponse(status=204)


@csrf_exempt
@login_required
def profile(request, name):
    profile = User.objects.get(username=name.split('-')[1])
    posts = Post.objects.filter(user=profile)
    posts = posts.order_by("-timestamp").all()

    rsp_data = {
        'user': {'requestor': request.user.username,
                 'username': profile.username,
                 'email': profile.email,
                 'followers': [f.username for f in profile.followers.all()]},
        'posts': [post.serialize() for post in posts]}

    return JsonResponse(rsp_data, safe=False)


@csrf_exempt
@login_required
def post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    post = Post(
        user = request.user,
        body = data.get("body", "")
    )
    post.save()

    return JsonResponse({"message": "Post was successful."}, status=201)


def _get_page_obj(posts):

    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 3)
    page_number = 1
    page = paginator.get_page(page_number)

    page_obj = {}
    page_obj['page'] = {'current': page_number, 'posts': [post.serialize() for post in page]}
    return page_obj


@csrf_exempt
@login_required
def following_posts(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    user = User.objects.get(username=request.user.username)
    posts = Post.objects.none()
    for f in user.following.all():
        posts = posts.union(posts, Post.objects.filter(user=f))

    return JsonResponse(_get_page_obj(posts), safe=False)


@csrf_exempt
@login_required
def posts(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)

    posts = Post.objects.all()
    return JsonResponse(_get_page_obj(posts), safe=False)


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
    return HttpResponseRedirect(reverse("index"))


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
