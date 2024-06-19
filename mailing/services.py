from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blog_from_cache():
    if not CACHE_ENABLED:
        return Blog.objects.filter(is_published=True)[:3]
    key = 'blog_list'
    blog = cache.get(key)
    if blog is not None:
        return blog
    blog = Blog.objects.filter(is_published=True)[:3]
    cache.set(key, blog)
    return blog
