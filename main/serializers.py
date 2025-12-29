from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ("id", "title", "content", "category", "image_url", "author", "date")

    def get_author(self, obj):
        if obj.user:
            return obj.user.username
        return "Padelin Aja Team"

    def get_date(self, obj):
        if obj.published_date:
            return obj.published_date.isoformat()
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        user = None
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        article = Article.objects.create(user=user, **validated_data)
        return article
