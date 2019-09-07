from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Count
from django.http import HttpResponse
import json
import pdb
import collections
import operator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



def new(request):
    context = {
            'form': PostForm(initial={'user': request.user})
    }
    return render(request, 'posts/new.html', context)


def create(request):
    context = {}
    if request.method == "POST":
       form = PostForm(request.POST, request.FILES or None)
       if form.is_valid():
           form.save()
    return redirect('home')


def edit(request, id):
    post = get_object_or_404(Post, pk=id)
    if 'id' is not None:
        context = {
            'post': post,
            'form': PostForm(instance=post)
        }
        return render(request, 'posts/edit.html', context)


def update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post)
        if form.is_valid():
            form.save()

        return redirect('home')


def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('home')


@login_required
@require_POST
def create_comment(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    message = request.POST.get('message')
    the_comment = Comment.objects.create(user=user, post=post, message=message)
    commentpk = the_comment.pk
    context = {
        'commentpk': commentpk
    }
    return HttpResponse(json.dumps(context), content_type = "application/json")


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('home')

@login_required
@require_POST
def like_toggle(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    is_like = user in post.likes.all()
    if is_like:
        post.likes.remove(user)
        result = "heart-empty"
        likes_count = post.likes.count()
    else:
        post.likes.add(user)
        result = "heart"
        likes_count = post.likes.count()
    context = {
        'result':result,
        'likes_count':likes_count

    }        
    return HttpResponse(json.dumps(context), content_type="application/json")


def search(request):
     return redirect('search')  


 
