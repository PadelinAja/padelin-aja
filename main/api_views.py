from rest_framework import generics, permissions
from .models import Article
from .serializers import ArticleSerializer


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    # Allow public reads and allow creating without authentication (user set to null)
    permission_classes = (permissions.AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
