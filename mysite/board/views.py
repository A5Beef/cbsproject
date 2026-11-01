from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def home(request):
    threads = Thread.objects.all().order_by("-created_at")

    return render(request, "board/home.html", {
        "threads": threads
    })

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "board/register.html", {
        "form": form
    })

@login_required
def create_thread(request):
    if request.method == "POST":
        title = request.POST.get("title")

        if title:
            thread = Thread.objects.create(
                title=title,
                author=request.user
            )
            return redirect("thread_detail", thread_id=thread.id)

    return render(request, "board/create_thread.html")

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    return render(request, "board/thread_detail.html", {
        "thread": thread
    })

@login_required
def create_reply(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Post.objects.create(
                thread=thread,
                author=request.user,
                content=content
            )
            
    return redirect("thread_detail", thread_id=thread.id)
