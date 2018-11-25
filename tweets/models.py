from django.db import models
from django.contrib.auth.models import User


class User(User):
    follows = models.ManyToManyField(User, related_name="followed_by")
    profil_resmi = models.ImageField(User, null=True)



class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

