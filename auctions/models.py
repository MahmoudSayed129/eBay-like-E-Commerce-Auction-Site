# from auctions.views import auction_view
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField, IntegerField
from django.utils import timezone

class User(AbstractUser):
    pass

class active_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    final_bid = models.IntegerField()
    title = models.CharField(max_length=64)
    img_url = models.CharField(default="null", max_length=64)
    description = models.CharField(max_length=64)
    category = models.CharField(default="null", max_length=64)
    date = models.DateTimeField(default=timezone.now)
    closed_auction = models.BooleanField(default='False')

    def __str__(self):
        return f"{self.title} of id {self.pk}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    auction_id = models.IntegerField(default="0")
    auction_item = models.ManyToManyField(active_list, blank=True)

    def __str__(self):
        return f"{self.user.username} made a bid of {self.bid_amount} on auction of id{self.auction_id}"
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_item = models.ManyToManyField(active_list, blank=True, related_name="auction")
    comment = models.CharField(max_length=256)
    auction_id = models.IntegerField(default="0")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.username} comment on auctio of id{self.auction_id}"

class WatchList (models.Model):
    auction_id = models.IntegerField(default="0")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_item = models.ManyToManyField(active_list, blank=True)
    
    def __str__(self):
        return f"auction of id {self.auction_id} is in {self.user.username}'s wathlist"


