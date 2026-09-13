from django.utils import timezone

from blog.models import Post


def get_published_posts():
    """Базовый QuerySet опубликованных постов с оптимизацией запросов."""
    return (
        Post.objects.select_related('location', 'author')
        .prefetch_related('category')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
        .order_by('-pub_date')
    )
