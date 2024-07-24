
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count

def blog(request):
    posts = BlogPost.objects.annotate(comment_count=Count('comments'))
    context = {'posts': posts ,
                }
    return render(request, 'blog/blog.html', context)


@login_required
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Blog added successfully')
            return redirect('blog:add_blog_post')
    else:
        form = BlogPostForm()
    return render(request, 'blog/add_blog_post.html', {'form': form})


def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    paginator = Paginator(comments, 5)  # Show 10 comments per page

    # Get total number of comments for the post
    total_comments = Comment.objects.filter(post=post).count()

    page_number = request.GET.get('page')
    comment_page = paginator.get_page(page_number)

    return render(request, 'blog/blog_details.html', {
        'post': post,
        'comment_page': comment_page,
        'form': CommentForm(),
        'total_comments': total_comments,
    })  

@login_required
def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:blog_detail', pk=post.pk)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    paginator = Paginator(comments, 10)  # Show 10 comments per page

    page_number = request.GET.get('page')
    comment_page = paginator.get_page(page_number)
    return render(request, 'blog/blog_details.html', {'form': form, 'post': post, 'comment_page': comment_page})


