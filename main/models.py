from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Article(models.Model):

    class CategoryChoices(models.TextChoices):
        BEGINNER = 'Beginner Guides', 'Beginner Guides'
        TECHNIQUE = 'Technique & Strategy', 'Technique & Strategy'
        FITNESS = 'Fitness & Warm-Ups', 'Fitness & Warm-Ups'
        COACHING = 'Coaching Insights', 'Coaching Insights'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices,
        default=CategoryChoices.BEGINNER
    )
    
    published_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Events(models.Model):
    
    class MatchType(models.TextChoices):
        FUN_MATCH = 'Fun Match', 'Fun Match'
        TURNAMEN = 'Turnamen', 'Turnamen'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=50,
        choices=MatchType.choices,
        default=MatchType.FUN_MATCH
    )
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')