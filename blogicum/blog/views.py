from django.shortcuts import get_object_or_404, render

from blog.models import Category
from blog.utils import get_published_posts

POSTS_LIMIT = 5


def index(request):
    post_list = get_published_posts()[:POSTS_LIMIT]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def detail(request, post_id):
    post = get_object_or_404(
        get_published_posts(),
        pk=post_id,
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_published_posts().filter(category=category)
    context = {
        'post_list': post_list,
        'category': category,
    }
    return render(request, 'blog/category.html', context)
