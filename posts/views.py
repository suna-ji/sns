from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Count
from django.http import HttpResponse
import json
import pdb
import collections
import operator



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


def create_comment(request, post_id):
    if request.method == "POST":
        user = request.user
        if user.is_anonymous:
            return redirect('account_login')
        post = get_object_or_404(Post, pk=post_id)
        message = request.POST.get('message')
        Comment.objects.create(user=user, post=post, message=message)
        return redirect('home')

# def create_comment(request):
#     if request.is_ajax():
#         user = request.user
#         if user.is_anonymous:
#             return redirect('account_login')
#         pk = request.POST.get('pk', None)    
#         post = get_object_or_404(Post, pk = post_id )
#         message = request.POST.get['message']
#         Comment.objects.create(user=user, post = post, message = message)
#         data = {'message':message}
#         return HttpResponse(json.dumps(data), "application/json")
#     return redirect('home')   




def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('home')


def like_toggle(request, post_id):
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')
    post = get_object_or_404(Post, pk=post_id)
    
    is_like = user in post.likes.all()
    
    if is_like:
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('home')


def post_like(request):
    pdb.set_trace()
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')   
    pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    post = get_object_or_404(Post, pk=pk)
    is_like = user in post.likes.all()
    if is_like:
        post.likes.remove(user)
        message = "좋아요 취소"
    else:
        post.likes.add(user)
        message = "좋아요"
    context = {'like_count': post.like_count,
               'message': message,
               }
    return HttpResponse(json.dumps(context), content_type="application/json")


def search(request):
     return redirect('search')  


 
