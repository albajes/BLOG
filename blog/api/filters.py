from django_filters import filters, ModelChoiceFilter

from blog.api.models import Blog, Tags, Post


class FilterBlog(filters.FilterSet):
    updated_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Blog
        fields = ['updated_at']


class FilterPost(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()
    tags = ModelChoiceFilter(queryset=Tags.objects.all())
    blog = ModelChoiceFilter(queryset=Blog.objects.all())

    class Meta:
        model = Post
        fields = ['created_at', 'tags', 'blog']