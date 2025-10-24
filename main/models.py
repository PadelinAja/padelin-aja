from django.db import models
import uuid
from django.contrib.auth.models import User

class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    price_range = models.CharField(max_length=100, blank=True, null=True)
    facilities = models.TextField(blank=True, null=True)
    image_url_2 = models.URLField(blank=True, null=True)
    image_url_3 = models.URLField(blank=True, null=True)
    image_url_4 = models.URLField(blank=True, null=True)
    image_url_5 = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name