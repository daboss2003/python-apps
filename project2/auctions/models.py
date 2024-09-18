
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    pass

    def bidding_history(self):
        return Bidding.objects.filter(user=self)




class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    def get_listings(self):
        return Listing.objects.filter(category=self)



class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=15)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='listings')
    reserve_price = models.DecimalField(max_digits=10,decimal_places=2)
    current_bid = models.DecimalField(max_digits=10,decimal_places=2)
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='listing_seller')
    end_time = models.DateTimeField()
    winner = models.ForeignKey(User,null=True, blank=True, on_delete=models.SET_NULL, related_name='won_listing')
    closed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    def update_current_bid(self,new_bid):
        if new_bid > self.current_bid:
            self.current_bid = new_bid
            self.save()
    def time_remaining(self):
        return max(self.end_time - timezone.now(),timezone.timedelta())        
    
class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_bidding')
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='listing_bid')
    bid_amount = models.DecimalField(max_digits=10,decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}-{self.listing.title}"
    
    def is_valid_bid(self):
        return self.bid_amount > self.listing.current_bid
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='listing_comment')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.username} by {self.listing.title}"
    
    def get_comment_for_listing(listing):
        return Comment.objects.filter(listing=listing)
    
    
    

    
class Image(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='listing_image')
    image_url = models.URLField()
    
    def __sts__(self):
        return f"{self.listing.title} - Image"
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_wishlist')
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='wish_listing')
    
    def __str__(self):
        return f"{self.listing.title} - Wishlist"
