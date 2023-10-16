from django.shortcuts import render
from django.views.generic import ListView

from BlogApp.models import Article


class ArticleListView(ListView):
    template_name = 'BlogApp/article_list.html'
    context_object_name = "articles"
    queryset = Article.objects.all()\
        .prefetch_related("tags")\
        .select_related("author", "category")




