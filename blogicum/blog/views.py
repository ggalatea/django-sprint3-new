from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'

    post_list = (
        Post.objects.select_related('location', 'author')
        .prefetch_related('category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
        .order_by('-pub_date')[:5]
    )

    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def detail(request, id):

    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True, pub_date__lte=timezone.now(), pk=id
        )
    )

    if not post.category.is_published:
        raise Http404()

    if post.pub_date > timezone.now():
        raise Http404()

    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    post_list = (
        Post.objects.select_related('location', 'author')
        .prefetch_related('category')
        .filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by('-pub_date')
    )
    context = {
        'post_list': post_list,
        'category': category,
    }
    return render(request, template, context)
