from django import forms

from blog.models import Blog
from common.views import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'body', 'image', 'is_published')