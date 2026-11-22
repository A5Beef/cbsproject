from django.shortcuts import render, redirect, get_object_or_404
from .models import Message, Thread, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q


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

@login_required
def edit_post(request, thread_id, post_id):
    thread = get_object_or_404(Thread, id=thread_id)
    post = get_object_or_404(
        Post,
        id=post_id,
        thread=thread,

        # Broken Access Control. Commented out ownership check. Uncomment code below for secure version.
        # Doesn't check ownership, resulting in other users being able to edit posts they don't own.
        author=request.user
        )

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            post.content = content
            post.save()
            return redirect("thread_detail", thread_id=thread.id)

    return render(request, "board/edit_post.html", {
        "thread": thread,
        "post": post
    })

@login_required
def delete_post(request, thread_id, post_id):
    thread = get_object_or_404(Thread, id=thread_id)
    post = get_object_or_404(
        Post,
        id=post_id,
        thread=thread,

        # Broken Access Control. Commented out ownership check. Uncomment code below for secure version.
        # Doesn't check ownership, resulting in other users being able to delete posts they don't own.
        author=request.user
        )

    if request.method == "POST":
        post.delete()
        return redirect("thread_detail", thread_id=thread.id)

    return render(request, "board/delete_post.html", {
        "thread": thread,
        "post": post
    })

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by("-created_at")

    return render(request, "board/inbox.html", {
        "messages": messages
    })

@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user).order_by("-created_at")

    return render(request, "board/sent_messages.html", {
        "messages": messages
    })

@login_required
def send_message(request):
    if request.method == "POST":
        recipient_id = request.POST.get("recipient")
        content = request.POST.get("content")

        if recipient_id and content:
            recipient = get_object_or_404(User, id=recipient_id)

            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )

            return redirect("sent_messages")

    users = User.objects.exclude(id=request.user.id)

    return render(request, "board/send_message.html", {
        "users": users
    })

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(
        Message,
        Q(sender=request.user) | Q(recipient=request.user),
        id=message_id
    )

    conversation_partner = (
        message.recipient
        if message.sender == request.user
        else message.sender
    )
    conversation = Message.objects.filter(
        Q(sender=request.user, recipient=conversation_partner)
        | Q(sender=conversation_partner, recipient=request.user)
    ).order_by("created_at")

    return render(request, "board/message_detail.html", {
        "message": message,
        "conversation": conversation,
        "conversation_partner": conversation_partner
    })
