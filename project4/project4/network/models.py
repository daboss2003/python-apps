
from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile")
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)

    def count_followers(self):
        return self.user.friend.count()
        
    
    def count_following(self):
        return self.user.user_friend.count() + self.user.friend.count()
    
    def serialize(self):
        return{
            'id': self.id,
            'user_id': self.user.id,
            'bio':self.bio,
            'profile_pics':self.profile_picture,
            'username':self.user.username,
            'user_email':self.user.email,
            
        }
    
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='post_storage/',blank=True,null=True)
    media_type = models.TextField(null=True)
    
    
    def like_count(self):
        return self.post_like.count()
    
    
    def comment_count(self):
        return self.post_comment.count()
    
    def serialize(self):
        return{
            'id':self.id,
            'user_id':self.user.id,
            'content':self.content,
            'media':self.media,
            'media_type':self.media_type,
            'timestamp':self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
   
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_comment")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def serialize(self):
        return{
            'id':self.id,
            'user_id':self.user.id,
            'post_id':self.post.id,
            'content':self.content,
            'timestamp':self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
    
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_like")
    is_like = models.BooleanField(default=False)
    
            
   
    
class Friend(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_friend')
    friend = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend')
    is_accepted = models.BooleanField(default=False)
    
    def serialize(self):
        return{
            'id':self.id,
            'user_id':self.user.id,
            'friend_id':self.friend.id,
            'is_friend':self.is_accepted,
        }
    
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    type = models.TextField(null=True)
    post = models.ForeignKey(Post,null=True,on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    
    def serialize(self):
        return{
            'id':self.id,
            'user_id':self.user.id,
            'type':self.type,
            'post_id':self.post.id,
            'content':self.content,
            'timestamp':self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            
        }
    

    
   

       