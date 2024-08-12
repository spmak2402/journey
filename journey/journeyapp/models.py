from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.


# class profile(models.Model):


class Profile(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='imgpro')
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    followers_no = models.IntegerField(default=0)
    folllowings_no = models.IntegerField(default=0)
    
class Triplog(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    caption = models.CharField(max_length=500, default = None)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    
    
    
    
    # def _str_(self):
        
    #     return self.caption
    
    # def increment_like(self):
        
    #     self.like_count += 1
    #     self.save()
    
class Likes(models.Model):
    
    Log_id = models.ForeignKey(Triplog, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Follow(models.Model):
    
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Comment(models.Model):
    
    triplog = models.ForeignKey(Triplog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    comments = models.CharField(max_length=800, default="comment here")
    created_at = models.DateTimeField(default=datetime.now)
    