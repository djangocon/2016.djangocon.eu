from django.views import generic

from .models import Post


class IndexView(generic.ListView):
    template_name = 'tinyblog/index.html'
    model = Post


class ArticleView(generic.DetailView):
    template_name = 'tinyblog/article.html'
    model = Post

    def get_object(self):
        return Post.objects.get(slug=self.kwargs['slug'])
